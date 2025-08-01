import os
import torch
import numpy as np
from PIL import Image
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer
from flask import render_template, url_for, jsonify, request, send_from_directory, Blueprint
from werkzeug.utils import secure_filename


TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))

script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "..", "models", "RealESRGAN_x2plus.pth")
model_path = os.path.normpath(model_path)


imgUpscaler_bp = Blueprint('imgUpscaler_bp', __name__, template_folder= TEMPLATE_DIR)

UPLOAD_FOLDER = os.path.join(script_dir, '..', 'static', 'Image_Upscaler', 'uploads')
OUTPUT_FOLDER = os.path.join(script_dir, '..', 'static', 'Image_Upscaler', 'outputs')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
use_half = True if torch.cuda.is_available() else False

model = RRDBNet(
    num_in_ch=3, num_out_ch=3, num_feat=64,
    num_block=23, num_grow_ch=32, scale=2
)

upsampler = RealESRGANer(
    scale=2,
    model_path=model_path,
    model=model,
    tile=0,
    tile_pad=10,
    pre_pad=0,
    half=use_half,
    device=device
)

@imgUpscaler_bp.route('/')
def index():
    return render_template('index_upscale.html', show_image = False)

@imgUpscaler_bp.route('/enhance', methods = ['POST'])
def enhance():
    if 'image' not in request.files:
        return jsonify({'error': 'No Image Uploaded'})
    
    file = request.files['image']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(input_path)

        img = Image.open(input_path).convert('RGB')
        img_np = np.array(img)

        output_np, _ = upsampler.enhance(img_np, outscale=2)

        ext = os.path.splitext(filename)[1].lower()
        name_wo_ext = os.path.splitext(filename)[0]
        output_filename = f"{name_wo_ext}_enhanced{ext}"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        Image.fromarray(output_np).save(output_path)

        img_url = f"http://localhost:5000/static/Image_Upscaler/outputs/{output_filename}"
        download_url = url_for('imgUpscaler_bp.download_file', filename = output_filename)

        return render_template('index_upscale.html', show_image = True, output_img = img_url, download_url = download_url)
    
    return jsonify({'error': 'Invalid file type'}), 400


@imgUpscaler_bp.route('/download/<filename>')
def download_file(filename):
    output_dir = os.path.abspath(OUTPUT_FOLDER)

    return send_from_directory(directory=output_dir, path=filename, as_attachment=True)
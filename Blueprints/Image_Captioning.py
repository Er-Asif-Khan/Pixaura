import os
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from flask import redirect, render_template, request, url_for, jsonify, Blueprint
from werkzeug.utils import secure_filename

imgCaptioning_bp = Blueprint('imgCaptioning_bp', __name__, template_folder = 'templates')

UPLOAD_FOLDER = 'static/Image_Captioning/uploads'
OUTPUT_FOLDER = 'static/Image_Captioning/outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok = True)
os.makedirs(OUTPUT_FOLDER, exist_ok = True)

ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

@imgCaptioning_bp.route('/')
def index():
    return render_template('index_caption.html', show_image = False)

@imgCaptioning_bp.route('/captionize', methods = ['POST'])
def captionize():
    if 'image' not in request.files:
        return jsonify({'error': 'No Image Uploaded'})
    
    file = request.files['image']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_path)

        img = Image.open(input_path).convert('RGB')
        inputs = processor(img, return_tensors = "pt")

        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens = True)

        output_filename = os.path.splitext(filename)[0] + '_caption.txt'
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        with open(output_path, 'w') as f:
            f.write(caption)

        img_url = url_for('static', filename = f'Image_Captioning/uploads/{filename}')
        print(img_url)

        return render_template('index_caption.html', show_image = True, image = img_url, caption = caption)
    
    return jsonify({'error': 'Invalid file type'}), 400



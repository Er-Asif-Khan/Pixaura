import os 
from rembg import remove
from PIL import Image
from flask import Blueprint, render_template, request, send_from_directory, url_for, jsonify
from werkzeug.utils import secure_filename

imgBgRemover_bp = Blueprint('imgBgRemover_bp', __name__, template_folder= 'templates', static_folder= 'static', static_url_path= '/BgRemover/static')

UPLOAD_FOLDER = 'Blueprints/Image_BgRemover/static/uploads'
OUTPUT_FOLDER = 'Blueprints/Image_BgRemover/static/outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok = True)
os.makedirs(OUTPUT_FOLDER, exist_ok = True)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@imgBgRemover_bp.route('/')
def index():
    return render_template('index4.html', show_image = False)

@imgBgRemover_bp.route('/removebg', methods = ['POST'])
def removebg():
    if 'image' not in request.files:
        return jsonify({'error': 'No Image Uploaded'}), 400
    
    file = request.files['image']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_path)

        name_wo_ext = os.path.splitext(filename)[0]
        output_filename = f"{name_wo_ext}_removedbg.png"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        try:
            with open(input_path, 'rb') as input_file:
                input_data = input_file.read()
                output_data = remove(input_data)

            with open(output_path, 'wb') as output_file:
                output_file.write(output_data)

            img_url = url_for('imgBgRemover_bp.static', filename = f'outputs/{output_filename}')
            download_url = url_for('imgBgRemover_bp.download_file', filename = output_filename)

            return render_template('index4.html', show_image = True, output_img = img_url, download_url = download_url)

        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    return jsonify({'error': 'Invalid File Format'}), 400

@imgBgRemover_bp.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment = True)



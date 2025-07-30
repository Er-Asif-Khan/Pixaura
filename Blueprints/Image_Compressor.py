import os
from flask import render_template, url_for, jsonify, request, send_from_directory, Blueprint
from PIL import Image
from werkzeug.utils import secure_filename

imgCompressor_bp = Blueprint('imgCompressor_bp', __name__, template_folder='templates')

UPLOAD_FOLDER = 'static/Image_Compressor/uploads'
OUTPUT_FOLDER = 'static/Image_Compressor/outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@imgCompressor_bp.route('/')
def index():
    return render_template("index_compress.html", show_image = False)

@imgCompressor_bp.route('/compress', methods = ['POST'])
def compress():
    if 'image' not in request.files or 'quality' not in request.form:
        return jsonify({'error': 'Missing Image or Quality value'}), 400
    
    file = request.files['image']
    quality = 100 - int(request.form['quality'])

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_path)

        name_wo_ext = os.path.splitext(filename)[0]
        file_ext = os.path.splitext(filename)[1].lower()
        output_filename = f"{name_wo_ext}_compressed{file_ext}"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        try:
            img = Image.open(input_path).convert("RGB")
            img.save(output_path, optimize = True, quality = quality)

            compressed_size = round(os.path.getsize(output_path) / 1024, 2)
            img_url = url_for('static', filename = f'Image_Compressor/outputs/{output_filename}')
            download_url = url_for('imgCompressor_bp.download_file', filename = output_filename)

            return render_template("index_compress.html", show_image = True, output_img = img_url, file_size = compressed_size, download_url = download_url)
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    return jsonify({'error': 'Invalid File Format'}), 400


@imgCompressor_bp.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment = True)
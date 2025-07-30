import cv2
import os
from flask import render_template, request, Blueprint, send_from_directory, url_for, jsonify
from werkzeug.utils import secure_filename

imgResizer_bp = Blueprint('imgResizer_bp', __name__, template_folder= 'templates')

UPLOAD_FOLDER = 'static/Image_Resizer/uploads'
OUTPUT_FOLDER = 'static/Image_Resizer/outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok = True)
os.makedirs(OUTPUT_FOLDER, exist_ok = True)

ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@imgResizer_bp.route('/')
def index():
    return render_template('index_resize.html', show_image = False)

@imgResizer_bp.route('/resize', methods = ['POST'])
def resize():
    if 'image' not in request.files:
        return jsonify({'error': 'No Image Uploaded'}), 400
    
    file = request.files['image']
    width = request.form.get('width')
    height = request.form.get('height')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_path)

        name_wo_ext = os.path.splitext(filename)[0]
        ext = os.path.splitext(filename)[1].lower()
        output_filename = f'{name_wo_ext}_resized{ext}'
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        try:
            img = cv2.imread(input_path)
            if img is None:
                return jsonify({'error': 'Invalid image'}), 400
            
            h, w = img.shape[:2]
            target_w, target_h = None, None

            if width and height:
                target_w = int(width)
                target_h = int(height)
            elif width:
                target_w = int(width)
                ratio = target_w / w
                target_h = int(h * ratio)
            elif height :
                target_h = int(height)
                ratio = target_h / h
                target_w = int(w * ratio)
            else:
                return jsonify({'error': 'Please provide width, height, or both'})
            
            resized = cv2.resize(img, (target_w, target_h))
            cv2.imwrite(output_path, resized)

            img_url = url_for('static', filename = f'Image_Resizer/outputs/{output_filename}')
            download_url = url_for('imgResizer_bp.download_file', filename = output_filename)

            return render_template('index_resize.html', show_image = True, output_img = img_url, download_url = download_url)
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    return jsonify({'error': 'Invalid file type'}), 400

@imgResizer_bp.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment = True)
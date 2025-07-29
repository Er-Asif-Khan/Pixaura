import os
import cv2
import numpy as np
from flask import Blueprint, render_template, request, send_from_directory, url_for, jsonify
from werkzeug.utils import secure_filename

imgBW2Color_bp = Blueprint('imgBW2Color_bp', __name__, template_folder='templates', static_folder='static', static_url_path='/Colorizer/static')

UPLOAD_FOLDER = 'Blueprints/Image_BW2Color/static/uploads'
OUTPUT_FOLDER = 'Blueprints/Image_BW2Color/static/outputs'
MODEL_DIR = 'Blueprints/Image_BW2Color/models'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok= True)

PROTOTXT = os.path.join(MODEL_DIR, 'colorization_deploy_v2.prototxt')
POINTS = os.path.join(MODEL_DIR, 'pts_in_hull.npy')
MODEL = os.path.join(MODEL_DIR, 'colorization_release_v2.caffemodel')

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
pts = np.load(POINTS).transpose().reshape(2, 313, 1, 1)

class8 = net.getLayerId("class8_ab")
conv8 = net.getLayerId("conv8_313_rh")
net.getLayer(class8).blobs = [pts.astype("float32")]
net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

@imgBW2Color_bp.route('/')
def index():
    return render_template("index5.html", show_image=False)

@imgBW2Color_bp.route('/colorize', methods=['POST'])
def colorize():
    if 'image' not in request.files:
        return jsonify({'error': 'No Image Uploaded'}), 400

    file = request.files['image']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_path)

        try:
            img = cv2.imread(input_path)
            scaled = img.astype("float32") / 255.0
            lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)

            resized = cv2.resize(lab, (224, 224))
            L = cv2.split(resized)[0]
            L -= 50

            net.setInput(cv2.dnn.blobFromImage(L))
            ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
            ab = cv2.resize(ab, (img.shape[1], img.shape[0]))

            L_original = cv2.split(lab)[0]
            colorized = np.concatenate((L_original[:, :, np.newaxis], ab), axis = 2)
            colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
            colorized = np.clip(colorized, 0, 1)
            output = (255 * colorized).astype("uint8")

            name_wo_ext = os.path.splitext(filename)[0]
            ext = os.path.splitext(filename)[1].lower()
            output_filename = f"{name_wo_ext}_colorized{ext}"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)
            cv2.imwrite(output_path, output)

            img_url = url_for('imgBW2Color_bp.static', filename=f'outputs/{output_filename}')
            download_url = url_for('imgBW2Color_bp.download_file', filename=output_filename)

            return render_template("index5.html", show_image=True, output_img=img_url, download_url=download_url)

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Invalid file type'}), 400

@imgBW2Color_bp.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

import os
import requests
from flask import Blueprint, render_template, request, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename

imgGenerator_bp = Blueprint('imgGenerator_bp', __name__, template_folder="templates", static_folder="static", static_url_path='/Generator/static')

UPLOAD_FOLDER = 'Blueprints/Image_Generator/static/outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

API_TOKEN = "my_token_which is pasted on clipboard and pinned"
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

@imgGenerator_bp.route('/')
def index():
    return render_template('index_gen.html', show_image=False)

@imgGenerator_bp.route('/generate', methods=['POST'])
def generate():
    prompt = request.form.get('prompt', '').strip()
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})

    if response.status_code == 200:
        output_filename = secure_filename("generated.png")
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)
        with open(output_path, "wb") as f:
            f.write(response.content)

        output_url = url_for('imgGenerator_bp.static', filename=f"outputs/{output_filename}")
        download_url = url_for('imgGenerator_bp.download_file', filename=output_filename)

        return render_template('index_gen.html', show_image=True, output_img=output_url, download_url=download_url)

    return jsonify({'error': f"Failed to generate image: HTTP {response.status_code}"}), response.status_code

@imgGenerator_bp.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))

from flask import Flask
from Blueprints.Image_Upscaler import imgUpscaler_bp

app = Flask(__name__, static_folder=static_path)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 
app.register_blueprint(imgUpscaler_bp, url_prefix = "/")

if __name__ == '__main__':
    app.run(debug = True, port = 5001)

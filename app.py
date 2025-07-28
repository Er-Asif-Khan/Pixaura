from flask import Flask
from Blueprints.Image_Captioning.Image_Captioning import imgCaptioning_bp
#from Blueprints.Image_Upscaler.Image_Upscaler import imgUpscaler_bp  # NOT Image_Upscaler directly

app = Flask(__name__)
app.register_blueprint(imgCaptioning_bp, url_prefix="/Captionize")
#app.register_blueprint(imgUpscaler_bp, url_prefix="/Upscaler")

if __name__ == '__main__':
    app.run(debug=True)

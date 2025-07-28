from flask import Flask
#from Blueprints.Image_Upscaler.Image_Upscaler import imgUpscaler_bp
from Blueprints.Image_Captioning.Image_Captioning import imgCaptioning_bp
from Blueprints.Image_Compressor.Image_Compressor import imgCompressor_bp

app = Flask(__name__)
#app.register_blueprint(imgUpscaler_bp, url_prefix="/Upscaler")
app.register_blueprint(imgCaptioning_bp, url_prefix="/Captionize")
app.register_blueprint(imgCompressor_bp, url_prefix="/Compressor")

if __name__ == '__main__':
    app.run(debug=True)

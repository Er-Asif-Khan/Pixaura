from flask import Flask
#from Blueprints.Image_Upscaler.Image_Upscaler import imgUpscaler_bp
from Blueprints.Image_Captioning import imgCaptioning_bp
from Blueprints.Image_Compressor import imgCompressor_bp
from Blueprints.Image_Resizer import imgResizer_bp
from Blueprints.Image_BgRemover import imgBgRemover_bp
from Blueprints.Image_BW2Color import imgBW2Color_bp
# from Blueprints.Image_Generator import imgGenerator_bp

app = Flask(__name__)
#app.register_blueprint(imgUpscaler_bp, url_prefix="/Upscaler")
app.register_blueprint(imgCaptioning_bp, url_prefix="/Captionize")
app.register_blueprint(imgCompressor_bp, url_prefix="/Compressor")
app.register_blueprint(imgResizer_bp, url_prefix="/Resizer")
app.register_blueprint(imgBgRemover_bp, url_prefix="/BgRemover")
app.register_blueprint(imgBW2Color_bp, url_prefix="/Colorizer")
# app.register_blueprint(imgGenerator_bp, url_prefix="/Generator")

if __name__ == '__main__':
    app.run(debug=True)

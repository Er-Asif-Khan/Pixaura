from flask import Flask, render_template
from Blueprints.Image_Captioning import imgCaptioning_bp
from Blueprints.Image_Compressor import imgCompressor_bp
from Blueprints.Image_Resizer import imgResizer_bp
from Blueprints.Image_BgRemover import imgBgRemover_bp
from Blueprints.Image_BW2Color import imgBW2Color_bp
from Blueprints.Image_ComicGen import imgComicGen_bp


app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 

app.register_blueprint(imgCaptioning_bp, url_prefix="/Captionize")
app.register_blueprint(imgCompressor_bp, url_prefix="/Compressor")
app.register_blueprint(imgResizer_bp, url_prefix="/Resizer")
app.register_blueprint(imgBgRemover_bp, url_prefix="/BgRemover")
app.register_blueprint(imgBW2Color_bp, url_prefix="/Colorizer")
app.register_blueprint(imgComicGen_bp, url_prefix="/Comic")


@app.route('/')
def index():
    return render_template('index_home.html')

if __name__ == '__main__':
   app.run(debug=True, port = 5000)

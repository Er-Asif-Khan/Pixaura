from flask import Flask, render_template, blueprints
from Blueprints.Image_Upscaler.Image_Upscaler import imgUpscaler_bp

app = Flask(__name__)
app.register_blueprint(imgUpscaler_bp)

if __name__ == '__main__':
    app.run(debug = True)
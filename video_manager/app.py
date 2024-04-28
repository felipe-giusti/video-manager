import os
from flask import Flask
import sys
from app.routes.render_routes import rendering_bp
from app.routes.video_routes import video_gen_bp
from app.routes.upload_routes import upload_bp

if 'debug' in sys.argv[1:]:
    from dotenv import load_dotenv
    load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET']

app.register_blueprint(rendering_bp)
app.register_blueprint(video_gen_bp, url_prefix='/videos')
app.register_blueprint(upload_bp, url_prefix='/upload')

if __name__ == "__main__":
    if 'debug' in sys.argv[1:]:
        app.run(host="localhost", port=8080)
    else:
        app.run(host="0.0.0.0", port=8080)
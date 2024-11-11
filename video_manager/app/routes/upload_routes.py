from flask import Blueprint

from app.use_cases import upload_uc

upload_bp = Blueprint("upload", __name__)
# prefix /upload


@upload_bp.route("/<video_id>", methods=["POST"])
def upload_video(video_id):
    upload_uc.uploadToYoutube(video_id)

    return "Sent to be uploaded", 200

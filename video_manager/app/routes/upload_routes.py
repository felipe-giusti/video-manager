from flask import Blueprint

from app.services import upload_service

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/<video_id>", methods=["POST"])
def upload_video(video_id):
    upload_service.uploadToYoutube(video_id)

    return "Sent to be uploaded", 200

from flask import Blueprint, render_template

from app import video_repo
from app.gen_enum import GenerationMethod

rendering_bp = Blueprint("render", __name__)


@rendering_bp.route("/")
def index():
    videos_metadata = []
    # TODO change later
    for sim_data in video_repo.get_all(GenerationMethod.SIMULATION_SHORT.value):
        sim_data = dict(sim_data)
        sim_data["_id"] = str(sim_data["_id"])
        sim_data["fid"] = str(sim_data["fid"])
        videos_metadata.append(sim_data)

    # print(videos_metadata)
    return render_template("index.html", videos_metadata=videos_metadata)


# forward / upload
@rendering_bp.route("/upload/<video_id>")
def forward_video(video_id):
    return render_template("upload.html", video_id=video_id)

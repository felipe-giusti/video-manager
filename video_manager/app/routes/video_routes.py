import logging

from flask import Blueprint, request, send_file

from app import video_repo
from app.gen_enum import GenerationMethod

video_gen_bp = Blueprint("videos", __name__)


@video_gen_bp.route("/", methods=["POST"])
def generate_video():
    gen_method = request.args.get("gen_method")
    if gen_method is None:
        return '"gen_method" query parameter required.', 400

    try:
        match gen_method:
            case GenerationMethod.SIMULATION_SHORT.value:
                video_repo.message_queue(GenerationMethod.SIMULATION_SHORT.value)

            case str(GenerationMethod.DEFAULT):
                for _, f in request.files.items():
                    # TODO change this later, don't need to store the data
                    video_repo.upload_raw_file(f, GenerationMethod.DEFAULT.value)

            case _:
                methods = [e.value for e in GenerationMethod]
                return f"Generation Method not implemented. \n Methods: {methods}", 400

    except Exception as e:
        logging.exception(e)
        return "Internal Server Error", 500

    return f"started {gen_method}", 200


# Route to serve video from MongoDB GridFS
@video_gen_bp.route("/<video_id>", methods=["GET"])
def serve_video(video_id):
    video = video_repo.get_video(video_id)
    return send_file(video, mimetype="video/mp4")


# delete
@video_gen_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    try:
        video_repo.delete_video(
            collection_name=GenerationMethod.SIMULATION_SHORT.value, fid=video_id
        )
    except Exception as e:
        logging.exception(e)
        return "Internal Server Error", 500

    return f"Video deleted ({video_id})", 200


# update
@video_gen_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id):
    updated_data = request.json["data"]
    if "fid" in updated_data:
        del updated_data["fid"]
    if "_id" in updated_data:
        del updated_data["_id"]

    try:
        # TODO change collection name later
        # video_repo.update_video(collection_name=GenerationMethod.SIMULATION_SHORT.value,
        #                         fid=video_id, data=updated_data)
        video_repo.delete_video(
            collection_name=GenerationMethod.SIMULATION_SHORT.value, fid=video_id
        )
        # send to be re-generated
        video_repo.message_queue(GenerationMethod.SIMULATION_SHORT.value, updated_data)

    except Exception as e:
        logging.exception(e)
        return "Internal Server Error", 500

    return "Video data updated", 200

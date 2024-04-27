import os
from flask import Flask, request, render_template, jsonify, send_file
from pymongo import MongoClient
import gridfs
import pika
from gen_enum import GenerationMethod
from repo.video_repo import VideoRepo
import sys
from bson import ObjectId
import logging


if 'debug' in sys.argv[1:]:
    from dotenv import load_dotenv
    load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET']

video_repo = VideoRepo()


@app.route('/')
def index():
    videos_metadata = []
    #TODO change later
    for sim_data in video_repo.get_all(GenerationMethod.SIMULATION_SHORT.value):
        sim_data = dict(sim_data)
        sim_data['_id'] = str(sim_data['_id'])
        sim_data['fid'] = str(sim_data['fid'])
        videos_metadata.append(sim_data)
    
    # print(videos_metadata)
    return render_template('index.html', videos_metadata=videos_metadata)


@app.route("/videos", methods=["POST"])
def hello_world():
    gen_method = request.args.get('gen_method')
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
@app.route('/videos/<video_id>', methods=["GET"])
def serve_video(video_id):
    video = video_repo.get_video(video_id)
    return send_file(video, mimetype='video/mp4')


# delete
@app.route('/videos/<video_id>', methods=['DELETE'])
def delete_video(video_id):
    try:
        video_repo.delete_video(collection_name=GenerationMethod.SIMULATION_SHORT.value,
                                fid=video_id)
    except Exception as e:
        logging.exception(e)
        return 'Internal Server Error', 500
        
    return f'Video deleted ({video_id})', 200

#update
@app.route('/videos/<video_id>', methods=['PUT'])
def update_video(video_id):

    updated_data = request.json['data']
    if 'fid' in updated_data:
        del updated_data['fid']
    if '_id' in updated_data:
        del updated_data['_id']

    try:
        #TODO change collection name later
        # video_repo.update_video(collection_name=GenerationMethod.SIMULATION_SHORT.value,
        #                         fid=video_id, data=updated_data)
        video_repo.delete_video(collection_name=GenerationMethod.SIMULATION_SHORT.value,
                                fid=video_id)
        # send to be re-generated
        video_repo.message_queue(GenerationMethod.SIMULATION_SHORT.value, updated_data)

    except Exception as e:
        logging.exception(e)
        return 'Internal Server Error', 500
    
    return 'Video data updated', 200


#forward / upload
@app.route('/upload/<video_id>', methods=['POST'])
def forward_video(video_id):
    try:
        video_repo.message_queue('upload', {'fid': video_id})
    except Exception as e:
        logging.exception(e)
        return 'Internal Server Error', 500
    
    return 'Video forwarded', 200


if __name__ == "__main__":
    if 'debug' in sys.argv[1:]:
        app.run(host="localhost", port=8080)
    else:
        app.run(host="0.0.0.0", port=8080)
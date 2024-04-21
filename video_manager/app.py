import os
from flask import Flask, request, render_template, jsonify, send_file
from pymongo import MongoClient
import gridfs
import pika
from gen_enum import GenerationMethod
from repo import video_repo
import sys
from bson import ObjectId


if 'debug' in sys.argv[1:]:
    from dotenv import load_dotenv
    load_dotenv()

app = Flask(__name__)

mongo_client = MongoClient(os.environ['MONGO_HOST'], 27017)

fs_raw = gridfs.GridFS(mongo_client['raw'])
upload_db = mongo_client["toUpload"]
fs_upload = gridfs.GridFS(upload_db)

#host will be specified by service name, find better way to do it later
mq_conn = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ['MQ_HOST']))
channel = mq_conn.channel()

@app.route("/generate/<gen_method>", methods=["POST"])
def hello_world(gen_method):
    err = None

    match gen_method:
        case GenerationMethod.SIMULATION_SHORT.value:
            err = video_repo.message_queue(channel, GenerationMethod.SIMULATION_SHORT.value)

        case str(GenerationMethod.DEFAULT):
            for _, f in request.files.items():
                err = video_repo.upload_file(f, fs_raw, channel, GenerationMethod.DEFAULT.value)

        case _:
            methods = [e.value for e in GenerationMethod]
            return f"Generation Method not implemented. \n Methods: {methods}", 400

    if err:
        return err
        
    return f"started {gen_method}", 200



@app.route('/')
def index():
    videos_metadata = []
    for  sim_data in upload_db['simulation'].find():
        sim_data = dict(sim_data)
        sim_data['_id'] = str(sim_data['_id'])
        videos_metadata.append(sim_data)
    # print(videos_metadata)
    return render_template('index.html', videos_metadata=videos_metadata, current_index=0)

# Route to serve video from MongoDB GridFS
@app.route('/video/<video_id>')
def serve_video(video_id):
    video_id = ObjectId(video_id)
    video = fs_upload.get(video_id)
    return send_file(video, mimetype='video/mp4')

@app.route('/delete_video', methods=['DELETE'])
def delete_video():
    # Logic to delete the video
    video_id = request.args.get('video_id')  # Optionally, you can pass the video ID as a query parameter
    # Perform deletion operation
    return 'Video deleted', 200

@app.route('/forward_video', methods=['POST'])
def forward_video():
    # Logic to forward the video
    video_id = request.args.get('video_id')  # Optionally, you can pass the video ID as a query parameter
    # Perform forwarding operation
    return 'Video forwarded', 200

@app.route('/update_video', methods=['PUT'])
def update_video():
    data = request.json
    video_id = data['videoId']
    updated_data = data['data']
    # Logic to update the video data
    return 'Video data updated', 200

if __name__ == "__main__":
    if 'debug' in sys.argv[1:]:
        app.run(host="localhost", port=8080)
    else:
        app.run(host="0.0.0.0", port=8080)
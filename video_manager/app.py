import os
from flask import Flask, request
from pymongo import MongoClient
import gridfs
import pika
from gen_enum import GenerationMethod
from repo import video_repo


app = Flask(__name__)

mongo_client = MongoClient("host.minikube.internal", 27017)

fs_raw = gridfs.GridFS(mongo_client.raw)

#host will be specified by service name, find better way to do it later
mq_conn = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
channel = mq_conn.channel()

@app.route("/generate/<gen_method>", methods=["POST"])
def hello_world(gen_method):


    if gen_method == GenerationMethod.PHYSICS_ART:
        pass

    else: #default

        for _, f in request.files.items():
            err = video_repo.upload(f, fs_raw, channel, GenerationMethod.DEFAULT.value)

            if err:
                return err
        
        return "Uploaded", 200







if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
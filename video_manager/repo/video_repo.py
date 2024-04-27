import json, pika
from bson import ObjectId
from pymongo import MongoClient
import gridfs
import os

#TODO add logger
#TODO change to util / common library

class VideoRepo:
    def __init__(self, client=None, mq_conn=None):
        if client is None:
            self.client = MongoClient(os.environ['MONGO_HOST'], 27017)
        else: self.client = client

        #TODO change raw later to pass stream of data or something
        self.fs_raw = gridfs.GridFS(self.client['raw'])
        self.db_upload = self.client["toUpload"]
        self.fs_upload = gridfs.GridFS(self.db_upload)

        #host will be specified by service name, find better way to do it later
        if mq_conn is None:
            mq_conn = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ['MQ_HOST']))
        self.mq_channel = mq_conn.channel()


    #TODO may delete function later.
    def upload_raw_file(self, file, queue_name:str):
        try:
            fid = self.fs_raw.put(file)
        except Exception as err:
            print("fs put error")
            raise

        message = {
            "raw_fid": str(fid)
        }

        try:

            self.mq_channel.queue_declare(queue=queue_name, durable=True)
            # print(f"basic publish to {queue_name} - message: {message}")
            self.mq_channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ),
            )

        except Exception as err:
            print("rabbitmq publish error")
            self.fs_raw.delete(fid)
            raise
        

    def message_queue(self, queue_name, message={}):
        try:

            self.mq_channel.queue_declare(queue=queue_name, durable=True)
            # print(f"basic publish to {queue_name} - message: {message}")
            self.mq_channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ),
            )

        except Exception as err:
            print("rabbitmq publish error")
            raise
        

    def delete_video(self, collection_name, fid: str|ObjectId):
        
        if not isinstance(fid, ObjectId):
            fid = ObjectId(fid)

        self.fs_upload.delete(fid)
        self.db_upload[collection_name].delete_one({"fid": fid})


    def update_video(self, collection_name, fid: str|ObjectId, data):
        if not isinstance(fid, ObjectId):
            fid = ObjectId(fid)

        #TODO Probably will change later how fid and _id are indexed later and instead of updating just recreate the document
        self.fs_upload.delete(fid)

        if '_id' in data:
            del data['_id']
        data['fid'] = fid

        self.db_upload[collection_name].update_one({'fid': fid}, {"$set": data})


    def get_video(self, fid: str|ObjectId):
        if not isinstance(fid, ObjectId):
            fid = ObjectId(fid)

        return self.fs_upload.get(fid)

    def get_all(self, collection_name):
        return self.db_upload[collection_name].find()
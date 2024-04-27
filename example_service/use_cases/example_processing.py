from repo import video_repo
from bson.objectid import ObjectId
from pymongo import MongoClient
import gridfs, os

mongo_client = MongoClient(os.environ.get("MONGO_HOST"), 27017)
fs_upload = gridfs.GridFS(mongo_client.toUpload)
fs_raw = gridfs.GridFS(mongo_client.raw)


def process(fid, mq_channel):

    file = fs_raw.get(ObjectId(fid))

    # do something...

    err = video_repo.upload(file, fs_upload, mq_channel, "to_upload")

    if err:
        return err


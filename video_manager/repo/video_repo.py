import json, pika

#TODO add logger

def upload(file, fs, mq_channel, queue_name:str):
    try:
        fid = fs.put(file)
    except Exception as err:
        print("fs put error")
        print(err)
        return "Internal Server Error", 500

    message = {
        "raw_fid": str(fid)
    }

    try:
        print(f"basic publish to {queue_name} - message: {message}")
        mq_channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )

    except Exception as err:
        print("rabbitmq publish error")
        print(err)
        fs.delete(fid)
        return "Internal Server Error", 500
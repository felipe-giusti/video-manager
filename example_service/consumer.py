import pika, sys, os
from use_cases import example_processing


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ.get("MQ_HOST")))
    channel = connection.channel()

    #TODO create common util/enum libraries
    channel.queue_declare(queue='default', durable=True)

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

        err = example_processing.process(body.get("fid"), ch)

        if err:
            channel.basic_nack(delivery_tag=method.delivery_tag)
        else:
            channel.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='default', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
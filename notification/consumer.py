import pika, sys, os, json
from use_cases.notification_builder import NotificationBuilder

if os.name == "nt": # check if running on windows:
    from use_cases.windows_notification import WindowsNotification
from use_cases.telegram_notification import TelegramNotification


def _is_service_active(service_env_str):
    return os.environ.get(service_env_str) in ("true", 1)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ.get("MQ_HOST")))
    channel = connection.channel()

    #TODO create common util/enum libraries
    channel.queue_declare(queue='to_upload', durable=True)

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
        try:
            body = json.loads(body.decode("utf-8").replace("'",'"'))

            builder = NotificationBuilder()
            # find better way to configure notifications later
            # maybe file or object that can be referenced through an api?

            if _is_service_active("HAS_WINDOWS_NOTIFICATION"):
            # forgot I was runnig it inside kubernetes cluster
            #TODO find out later if there's a workaround to make this work
                if os.name == "nt": # check if running on windows
                    builder.add(WindowsNotification)
            
            if _is_service_active("HAS_TELEGRAM_NOTIFICATION"):
                builder.add(TelegramNotification)

            builder.notify_all(body)

            channel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            import traceback
            traceback.print_exception(e)


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
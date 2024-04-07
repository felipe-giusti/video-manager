import json
from use_cases.notification_builder import NotificationBuilder
from use_cases.telegram_notification import TelegramNotification

from dotenv import load_dotenv
load_dotenv()

def _is_service_active(string):
    return True

def test(body):
    body = json.loads(body.decode("utf-8").replace("'",'"'))

    builder = NotificationBuilder()
    # find better way to configure notifications later
    # maybe file or object that can be referenced through an api?

    # if _is_service_active("HAS_WINDOWS_NOTIFICATION"):
    # # forgot I was runnig it inside kubernetes cluster
    # #TODO find out later if there's a workaround to make this work
    #     if os.name == "nt": # check if running on windows
    #         builder.add(WindowsNotification)
    
    if _is_service_active("HAS_TELEGRAM_NOTIFICATION"):
        builder.add(TelegramNotification)

    builder.notify_all(body)

test(json.dumps({"queue": "yes"}).encode())
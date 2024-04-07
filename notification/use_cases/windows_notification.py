from use_cases.notification_interface import NotificationService
from winotify import Notification
import os


class WindowsNotification(NotificationService):

    def notify(self, msg):
        msg = str(msg)
        toast = Notification(app_id="video-manager",
                            title="Video Ready",
                            msg=msg,
                            duration="short")
        
        toast.add_actions(
            label="open view",
            # launch = "http://localhost:8080/videos")
            launch=f"http://{os.environ.get("APP_HOST")}:{os.environ.get("APP_PORT")}/{os.environ.get("APP_VIEW_ROUTE")}")

        toast.show()
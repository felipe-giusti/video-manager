from typing import Set
from use_cases.notification_interface import NotificationService

## will create intended notifications and send them
class NotificationBuilder:

    
    def __init__(self, services: Set[NotificationService]=None) -> None:
        """_summary_
        Args:
            service_list (List[NotificationService], optional): List of notification service instances.
            The service must implement the NotificationService interface.
            Defaults to None.
        """

        if not services:
            self.services = set()


    def add(self, service: NotificationService):
        print(service)
        if issubclass(service, NotificationService):
            self.services.add(service)
            print(self.services)
        else:
            print("not")
            # maybe raise custom exception later


    def notify_all(self, message):
        for service in self.services:
            service().notify(message)
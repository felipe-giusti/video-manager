from abc import ABC, abstractmethod

class NotificationService(ABC):
    
    @abstractmethod
    def notify(self, message):
        pass
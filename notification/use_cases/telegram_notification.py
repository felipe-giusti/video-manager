from use_cases.notification_interface import NotificationService
import telegram
import os
import asyncio


class TelegramNotification(NotificationService):

    def notify(self, message):
        message = str(message)

        self.bot = telegram.Bot(token=os.environ.get("TELEGRAM_TOKEN"))

        asyncio.run(self.send_message(message))

        # could add functionality later to manage via this bot
    
    async def send_message(self, message):
        await self.bot.send_message(chat_id=os.environ.get("TELEGRAM_CHANNEL_ID"),
                         text=message)

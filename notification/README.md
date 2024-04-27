# Notification

Notificaiton Service.

For now it sends a message via Telegram to notice the user.

The Service is subscribed to a queue in RabbitMQ, so it will send the notifications when a message is published to it.

I don't plan on working on this for now, as it is not important for the core of the application, I may change it or improve it in the future.
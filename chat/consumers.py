import logging

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json

# Configure the logger
logging.basicConfig(
    level=logging.ERROR,  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s [%(levelname)s]: %(message)s',  # Define the log message format
    filename='app.log',  # Specify a log file
    filemode='w'  # Log file mode (append or write)
)


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_id = None
        self.room_name = None
        self.room_group_name = None

    async def connect(self):
        try:
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            self.room_group_name = f"chat_{self.room_name}"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        except Exception as e:
            logging.error(f"Connection error: {e}")

    @sync_to_async
    def get_chat_by_id(self):
        try:
            from .models import ChatRoom
            return ChatRoom.objects.filter(id=self.room_id).first()
        except self.room_id.DoesNotExist as e:
            logging.error(f"ChatRoom does not exist: {e}")

    @sync_to_async
    def create_message(self, chat_room, message):
        try:
            from .models import Message
            logging.error(f"USER: {self.scope['user'] if self.scope['user'] else None}")
            return Message.objects.create(room=chat_room, sender=self.scope['user'] if self.scope['user'] else Noney, content=message)
        except Exception as e:
            print("Message could not be created:", e)
            logging.error(f"No message created: {e}")

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json["message"]
            chat_room = await self.get_chat_by_id()
            message = await self.create_message(chat_room, message)
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat.message", "message": message}
            )
        except Exception as e:
            logging.error(f"Receive error: {e}")

    async def chat_message(self, event):
        try:
            message = event["message"]
            await self.send(text_data=json.dumps({"message": message}))
        except Exception as e:
            logging.error(f"Chat message error: {e}")

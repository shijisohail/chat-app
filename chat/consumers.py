import logging
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
import sys

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Set the global log level

# Create a formatter
formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')

# Create a console handler and set the log level
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)  # Set the log level for console output

# Set the formatter for the console handler
console_handler.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(console_handler)


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_id = None
        self.room_name = None
        self.room_group_name = None
        self.user = None

    async def connect(self):
        try:
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            self.room_group_name = f"chat_{self.room_name}"
            self.user = self.scope["user"]
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        except Exception as e:
            logging.error(f"Connection error: {e}")

    # async def disconnect(self, code):
    #     try:
    #         print(f"Disconnect from {self.room_group_name}")
    #     except Exception as e:
    #         logging.error(f"Disconnect Error: {e}")

    # @websocket_authorization
    @sync_to_async
    def get_chat_by_id(self):
        try:
            from .models import ChatRoom
            return ChatRoom.objects.filter(name=self.room_name).first()
        except self.room_id.DoesNotExist as e:
            logging.error(f"ChatRoom does not exist: {e}")

    @database_sync_to_async
    def create_message(self, chat_room, message):
        try:
            from .models import Message
            logging.debug(f"USER: {self.scope['user'] if self.scope['user'] else None}")
            Message.objects.create(room=chat_room, user=self.scope['user'] if self.scope['user'] else None, content=message)
            return f"{self.scope['user'].first_name if self.scope['user'] else None}: {message}"
        except Exception as e:
            logging.error(f"No message created: {e}")

    async def receive(self, text_data):
        try:
            await database_sync_to_async(self.scope["session"].save)()
            message = text_data
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

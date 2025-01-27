import logging
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
from channels_sockets.settings import logger


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
            # old_messages = await self.retrieve_messages(room_id)
            # await self.send(text_data=json.dumps({"old_messages": old_messages}))
        except Exception as e:
            logger.error(f"Connection error: {e}")

    async def retrieve_messages(self, room_id):
        from .models import Message
        try:
            messages = Message.objects.filter(room_id=room_id).values_list('content', flat=True).order_by('-timestamp')
            return list(messages)
        except Message.DoesNotExist:
            logger.error(f'Message does not exist for room {room_id}')
            return []

    async def disconnect(self, code):
        try:
            print(f"Disconnect from {self.room_group_name}")
        except Exception as e:
            logging.error(f"Disconnect Error: {e}")

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
            Message.objects.create(room=chat_room, user=self.scope['user'] if self.scope['user'] else None, content=message)
            return f"{self.scope['user'].first_name if self.scope['user'] else None}: {message}"
        except Exception as e:
            logging.error(f"No message created: {e}")

    async def chat_typing(self, event):
        try:
            typing_status = event["typing_status"]
            await self.send(text_data=json.dumps({"typing_status": typing_status}))
        except Exception as e:
            logger.error(f"Chat typing error: {e}")

    async def broadcast_typing_status(self, typing_status):
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.typing", "typing_status": f'{typing_status}'}
        )

    async def receive(self, text_data):
        from chat.helpers import retrieve_messages
        try:
            await database_sync_to_async(self.scope["session"].save)()
            if text_data.startswith('typing_status:'):
                typing_status = text_data.split(':')[1]
                await self.broadcast_typing_status(typing_status)
            elif text_data == 'retrieve_messages':
                previous_messages = await retrieve_messages(self.room_name)
                await self.send(text_data=json.dumps({"previous_messages": previous_messages}))
            else:
                message = text_data
                chat_room = await self.get_chat_by_id()
                message = await self.create_message(chat_room, message)
                await self.channel_layer.group_send(
                    self.room_group_name, {"type": "chat.message", "message": message}
                )
        except Exception as e:
            logger.error(f"Receive error: {e}")

    async def chat_message(self, event):
        try:
            message = event["message"]
            await self.send(text_data=json.dumps({"message": message}))
        except Exception as e:
            logging.error(f"Chat message error: {e}")


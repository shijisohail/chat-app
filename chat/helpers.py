import json

from channels.db import database_sync_to_async

from channels_sockets.settings import logger

from .models import Message


@database_sync_to_async
def retrieve_messages(name):
    try:
        messages = Message.objects.filter(room__name=name)
        return [
            f"{name} : {content}"
            for name, content in messages.values_list(
                "user__first_name", "content"
            ).order_by("timestamp")
        ]
    except Message.DoesNotExist:
        logger.error(f"Message does not exist for room {name}")
        return []

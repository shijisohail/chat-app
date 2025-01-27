from django.shortcuts import render
from .models import ChatRoom
from channels_sockets.settings import logger


def room_register(request):
    return render(request, "../templates/room_register.html")


def room(request, room_name):
    try:
        chat = ChatRoom.objects.get_or_create(name=room_name)
        logger.info("CHATTTTT", chat)
        return render(request, "../templates/room.html", {"room_name": room_name})
    except Exception as e:
        logger.error("EXC", e)


def homepage(request):
    return render(request, "../templates/homepage.html")

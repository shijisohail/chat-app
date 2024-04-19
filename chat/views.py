from django.shortcuts import render
from .models import ChatRoom


def room_register(request):
    return render(request, "../templates/room_register.html")


def room(request, room_name):
    try:
        chat = ChatRoom.objects.create(name=room_name)
        print("CHATTTTT", chat)
        return render(request, "../templates/room.html", {"room_name": room_name})
    except Exception as e:
        print("EXC", e)

def homepage(request):
    return render(request, "../templates/homepage.html")

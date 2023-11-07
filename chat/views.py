from django.shortcuts import render


def room_register(request):
    return render(request, "../templates/room_register.html")


def room(request, room_name):
    return render(request, "../templates/room.html", {"room_name": room_name})


def homepage(request):
    return render(request, "../templates/homepage.html")

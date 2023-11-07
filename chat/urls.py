from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage),
    path("room-register/", views.room_register, name="room-register"),
    path("<str:room_name>/", views.room, name="chat-room"),
]

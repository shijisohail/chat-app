from django.db import models

from user.models import User


class ChatRoom(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, null=False, blank=False
    )
    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, null=False, blank=False
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

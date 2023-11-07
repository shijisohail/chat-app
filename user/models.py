from django.db import models
import uuid
# Create your models here.


class UserType:
    SUPER_ADMIN = 1
    ADMIN = 2
    USER_TYPE = [
        (SUPER_ADMIN, 'SUPER_ADMIN'),
        (ADMIN, 'ADMIN'),
    ]


class Status:
    DELETED = 0
    ACTIVE = 1
    INACTIVE = 2
    BLOCKED = 3
    STATUS = [
        (DELETED, 'DELETED'),
        (ACTIVE, 'ACTIVE'),
        (INACTIVE, 'INACTIVE'),
        (BLOCKED, 'BLOCKED')
    ]

    @classmethod
    def get_status_name(cls, type_id):
        return dict(cls.STATUS).get(type_id)


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(null=True, blank=True, max_length=100)
    last_name = models.CharField(null=True, blank=True, max_length=100)
    username = models.CharField(null=False, blank=False, max_length=200)
    email = models.EmailField(unique=True, null=False, blank=False)
    status = models.CharField(max_length=1, choices=Status.STATUS, default=Status.ACTIVE)
    user_type = models.CharField(max_length=1, choices=UserType.USER_TYPE, default=UserType.SUPER_ADMIN)
    phone_number = models.BigIntegerField(blank=True, null=True)
    password = models.CharField(null=False, blank=False, max_length=250)

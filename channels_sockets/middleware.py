import traceback

import django.db
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.conf import settings
from jwt import DecodeError, ExpiredSignatureError, InvalidSignatureError
from jwt import decode as jwt_decode


class JWTAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        from django.contrib.auth.models import AnonymousUser

        django.db.close_old_connections()
        try:
            authorization = scope.get("query_string")
            if authorization:
                jwt_token = authorization.decode("utf8").split("=")[1]

                jwt_payload = self.get_payload(jwt_token)
                user_credentials = self.get_user_credentials(jwt_payload)
                user = await self.get_logged_in_user(user_credentials)
                scope["user"] = user
            else:
                scope["user"] = AnonymousUser()
        except (InvalidSignatureError, KeyError, ExpiredSignatureError, DecodeError):
            traceback.print_exc()
            scope["user"] = AnonymousUser()
            return await self.app(scope, receive, send)

    def get_payload(self, jwt_token):
        payload = jwt_decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload

    def get_user_credentials(self, payload):
        """
        method to get user credentials from jwt token payload.
        defaults to user id.
        """
        user_id = payload["user_id"]
        return user_id

    async def get_logged_in_user(self, user_id):
        user = await self.get_user(user_id)
        return user

    @database_sync_to_async
    def get_user(self, user_id):
        from django.contrib.auth.models import AnonymousUser

        from user.models import User

        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()


def jwt_auth_middleware_stack(app):
    return JWTAuthMiddleware(AuthMiddlewareStack(app))

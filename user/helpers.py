from rest_framework_simplejwt.tokens import RefreshToken
from channels.db import database_sync_to_async
import logging


def websocket_authorization(func):
    async def wrapper(self, *args, **kwargs):
        try:
            token = self.scope.get('query_string').decode("utf-8").split("=")[1]
            user = await get_user_from_token(token)
            if user is not None:
                self.scope['user'] = user
                return await func(self, *args, **kwargs)
            else:
                await self.close()
        except Exception as e:
            logging.error(f"Authorization error: {e}")
            await self.close()

    return wrapper


@database_sync_to_async
def get_user_from_token(token):
    try:
        refresh_token = RefreshToken(token)
        user = refresh_token.user
        return user
    except Exception as e:
        logging.error(f"Error getting user from token: {e}")
        return None

"""
ASGI config for channels_sockets project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels_sockets.middleware import jwt_auth_middleware_stack
from chat.routing import websocket_urlpatterns
import django

django.setup()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "channels_sockets.settings")
chat_socket_app = get_asgi_application()


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": jwt_auth_middleware_stack(
            URLRouter(
                websocket_urlpatterns,
            )
        ),
    }
)

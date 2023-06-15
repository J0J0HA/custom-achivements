"""
ASGI config for customachivements project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import OriginValidator
import achievements.routing
from achievements.middleware import HeaderMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "customachivements.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": OriginValidator(
            HeaderMiddleware(
                AuthMiddlewareStack(
                    URLRouter(achievements.routing.websocket_urlpatterns)
                )
            ),
            allowed_origins=["*"],
        ),
    }
)

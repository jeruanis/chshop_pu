"""
ASGI config for shopme project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""


import os
from decouple import config
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import re_path, path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f'{config("PROJECT_NAME")}.settings')
django_asgi_app = get_asgi_application()

from chatapp import consumers
from notification import nconsumers

application = ProtocolTypeRouter({
  "http": django_asgi_app,
  'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
        URLRouter([
            path('chatapp/<int:room_id>/', consumers.ChatConsumer.as_asgi()),
            path('', nconsumers.NotificationConsumer.as_asgi()),
            # re_path(r'ws/chatapp/(?P<room_name>\w+)/$', chatapp.consumers.ChatConsumer.as_asgi()),
			# re_path(r'', notification.nconsumers.NotificationConsumer.as_asgi()),
        ])
    )
    ),
})

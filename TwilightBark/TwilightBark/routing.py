""" Channel router to route messages to correct channel """
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path
from chat.consumers import ChatConsumer


# Top level ASGI application stack - dispatch to other apps like websockets
application = ProtocolTypeRouter({
    # Using websocket protocol with security based on ALLOWED_HOSTS in settings
    'websocket': AllowedHostsOriginValidator(
        # Allow users connecting to websocket to be authenticated
        AuthMiddlewareStack(
            # Declare views/paths handling websocket connections
            URLRouter([
                path('ws/chat/<room_name>/', ChatConsumer.as_asgi()),
            ])
        )
    )
})

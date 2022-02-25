""" """
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path
from chat.consumers import ChatConsumer


# jjfjfd
application = ProtocolTypeRouter({
    # Declare that using websocket protocol with security based on ALLOWED_HOSTS
    'websocket': AllowedHostsOriginValidator(
        # Allow users connecting to websocket to be authenticated
        AuthMiddlewareStack(
            # Declare views/paths handling websocket connections
            URLRouter([
                # path('', ChatConsumer()),
                path('ws/chat/<room_name>/', ChatConsumer.as_asgi()),
            ])
        )
    )
})

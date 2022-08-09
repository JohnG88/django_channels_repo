"""
ASGI config for channelsite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

# Next strep is to point the root routing confg at the chat.routing module

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'channelsite.settings')

# Initialize Django ASGI application early to ensure the AppRegistry is populated before importing code that may import ORM models
django_asgi_app = get_asgi_application()

import chat.routing

'''
    This routing config specifies that when a connection is made to the Channels development server, the ProtocolTypeRouter will first inspect the type of connection. If it is a websocket connection(ws:// or wss://), the conn will be given to the AuthMiddleWare
'''
'''
    The AuthMiddlewareStack will populate the conn's scope with a reference to the currently authenticated user similar to how Django's AuthenticationMiddleware populates the request object of a view function with the currently authenticated user. Then the connection will be given o the URLRouter.
'''
'''
    The URLRouter will examine the HTTP path of the conn to route it to a particular consumer, based on the provided url patterns 
'''

application = ProtocolTypeRouter({
    # Just HTTP for now.(We can add other protocols later.)
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
        )
    ),
})

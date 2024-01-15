from django.urls import path

from .consumer import CarConsumer

websocket_urlpatterns = [
    path('', CarConsumer.as_asgi())
]

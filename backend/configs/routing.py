from channels.routing import URLRouter

from django.urls import path

from apps.cars.routing import websocket_urlpatterns as car_router
from apps.chat.routing import websocket_urlpatterns as chat_router

websocket_urlpatterns = [
    path('api/chat/', URLRouter(chat_router)),
    path('api/cars/', URLRouter(car_router))
]
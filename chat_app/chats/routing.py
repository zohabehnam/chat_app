 
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/<str:token>/', consumers.ChatConsumer.as_asgi()),
    path('ws/notify/<str:token>/', consumers.NotificationConsumer.as_asgi()),

]
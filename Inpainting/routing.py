from django.urls import path
from Inpainting.consumers import ChatConsumer

websocket_urlpatterns = [
    ('ws/chat/', ChatConsumer)
]

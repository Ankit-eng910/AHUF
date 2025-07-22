from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/order-tracking/<str:order_id>/', consumers.OrderTrackingConsumer.as_asgi()),
]
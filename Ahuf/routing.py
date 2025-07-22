from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import Ahuf_app.routing  # import your app's websocket routes

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            Ahuf_app.routing.websocket_urlpatterns
        )
    ),
})
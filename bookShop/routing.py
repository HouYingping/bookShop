from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import myapp.routing
# protocolTypeRouter:ASGI支持多种不同的协议，这里只使用websocket协议

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    #AuthMiddlewareStack djangode channels封装了django 的 auth模块
    'websocket': AuthMiddlewareStack(
        # 指定路由文件的路径，也可以直接将路由信息写在这里
        URLRouter(
            myapp.routing.websocket_urlpatterns
        )
    ),
})
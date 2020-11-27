# from asgiref.sync import async_to_sync
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
import json

consumer_object_list = []
# consumer类似django中的view
# 同步类
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # self.scope()类似于django中的request，包含了请求的type、path、header、cookie、session、user等等有用的信息
        if self not in consumer_object_list:
            print("我连上了")
            self.accept()
            consumer_object_list.append(self)

    def disconnect(self, close_code):
        consumer_object_list.remove(self)
        raise StopConsumer()        # 主动报异常 无需做处理 内部自动捕获

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # self.send(text_data=json.dumps({
        #     "message": "客服回复："+message
        # }))
        from myapp.views.users import u_id
        for i in range(len(consumer_object_list)):
            obj = consumer_object_list[i]
            obj.send(text_data=json.dumps({
                "id":u_id,
                "message": message
        }))
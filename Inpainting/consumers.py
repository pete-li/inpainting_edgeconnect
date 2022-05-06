# from channels.generic.websocket import WebsocketConsumer  #同步
from channels.generic.websocket import AsyncWebsocketConsumer  #异步
import json
import time


class ChatConsumer(AsyncWebsocketConsumer):
    # websocket建立连接时执行方法
    async def connect(self):
        await self.accept()

    # websocket断开时执行方法
    async def disconnect(self, close_code):
        print(close_code)

    # 从websocket接收到消息时执行函数
    async def receive(self, text_data):
        for i in range(10):
            time.sleep(i)
            message = '结果: ' + str(i)
            text_data=json.dumps({'message': message})
            print('text_data: ',text_data)
            await self.send(text_data)

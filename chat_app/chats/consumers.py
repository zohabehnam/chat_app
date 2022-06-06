from channels.generic.websocket import  AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer
import json
import ast
from jwt import decode as jwt_decode
from config import settings
from config.redisConnection import redis_conn


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.user_token = self.scope['url_route']['kwargs']['token']
            decoded_data = jwt_decode(self.user_token, settings.SECRET_KEY, algorithms=["HS256"])
            self.user=str(decoded_data['user_id'])
    

            await self.channel_layer.group_add(
                self.user,
                self.channel_name
            )

            # return await super().connect()
            await self.accept()
            redis_conn.set(f"{self.user}_is_online",1)

            messages = redis_conn.hgetall(f"{self.user}_messages")
            for message in messages.values():
                res = ast.literal_eval(message)
                
                await self.channel_layer.group_send(
                    self.user,
                    {
                        'type': 'chat_message',
                        'message':json.dumps(res) 
                    }
                )
            redis_conn.delete(f"{self.user}_messages")





        except:
            await self.close()
    
    async def disconnect(self, close_code):
        await self.send(text_data="bye")
        await self.channel_layer.group_discard(
            self.user,
            self.channel_name
        )
        redis_conn.delete(f"{self.user}_is_online")

        

    # async def receive(self, text_data=None, bytes_data=None):
    #     if text_data:
    #         text_data_json = json.loads(text_data)
    #         receiver = text_data_json['receiver']
    #         user_group_name = f"{username}"
            
    #         await self.channel_layer.group_send(
    #             user_group_name,
    #             {
    #                 'type': 'chat_message',
    #                 'message': text_data
    #             }
    #         )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=message)
        
    async def notify(self, event):
        pass

    


class NotificationConsumer(AsyncJsonWebsocketConsumer):


    async def connect(self):

      
        try:
            self.user_token = self.scope['url_route']['kwargs']['token']
            decoded_data = jwt_decode(self.user_token, settings.SECRET_KEY, algorithms=["HS256"])
            self.user=str(decoded_data['user_id'])
            await self.channel_layer.group_add(
                self.user,
                self.channel_name
            )

            await self.accept()
            redis_conn.set(f"{self.user}_is_online",1)
            notifications = redis_conn.hgetall(f"{self.user}_notifications")
            for notif in notifications.values():
                res = ast.literal_eval(notif)
                await self.channel_layer.group_send(
                    self.user,
                    {
                        'type': 'notify',
                        'message':json.dumps(res) 
                    }
                )
            redis_conn.delete(f"{self.user}_notifications")
        
        except:
            await self.close()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.user,
            self.channel_name
        )
        redis_conn.delete(f"{self.user}_is_online")

    async def notify(self, event):
        await self.send_json(event)

    async def chat_message(self, event):
        pass


from channels.generic.websocket import  AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
import json

from jwt import decode as jwt_decode

from config import settings


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
			return await super().connect()
		except:
			await self.close()
	
	async def disconnect(self, close_code):
		await self.send(text_data="bye")
		await self.channel_layer.group_discard(
			self.user,
			self.channel_name
		)

		

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
			return await super().connect()
		except:
			await self.close()
	
	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.user,
			self.channel_name
		)

	async def notify(self, event):
	    await self.send_json(event)
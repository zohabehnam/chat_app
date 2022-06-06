from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from accounts.models import User
from chats.models import Notifications
import uuid


"""  redis connection """
from config.redisConnection import *


def notify(self,sender, receiver, action_type):
    channel_layer = get_channel_layer()
    group_name = f"{receiver}"
    is_online=redis_conn.get(f"{receiver}_is_online")
    if is_online is  None:
        redis_conn.hsetnx(f'{receiver}_notifications', str(uuid.uuid4()), str({'sender': sender ,'receiver':receiver,'action_type':action_type}))
    async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'notify',
                    'message': json.dumps({'sender': sender, 'receiver': receiver, 'action_type':action_type})
                }
            )
    Notifications.objects.create(sender = User.objects.get(id=sender), receiver=User.objects.get(id=receiver),action_type=action_type)      
        
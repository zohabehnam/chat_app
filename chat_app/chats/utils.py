from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from accounts.models import User

from chats.models import Notifications


def notify(self,sender, receiver, type):
    channel_layer = get_channel_layer()
    group_name = f"{receiver}"
    async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'notify',
                    'message': json.dumps({'sender': sender, 'receiver': receiver, 'type':type})
                }
            )
    Notifications.objects.create(sender = User.objects.get(id=sender), receiver=User.objects.get(id=receiver),type=type)
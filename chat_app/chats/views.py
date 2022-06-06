from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from rest_framework import status
from .models import Message, Notifications
from accounts.models import User
from django.db.models import Q
from .serializers import MessageSerializer, NotificationSerializer
import uuid
import redis

"""  redis connection """
# redis_conn = redis.Redis(host='redis-15943.c80.us-east-1-2.ec2.cloud.redislabs.com', port=15943,
#           decode_responses=True, password='ouqodOS7Zr7LiS02eKOIywzmK6Xr8ToB')


redis_conn = redis.Redis(host='redis', port=6379, decode_responses=True) 


class NewMessage(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        if (not "receiver" in request.data) :
            return Response({'receiver': 'receiverid is required'}, status=status.HTTP_400_BAD_REQUEST)           
        if not "text" in request.data:
            return Response({'text': 'text is required'}, status=status.HTTP_400_BAD_REQUEST)            

        user = request.user.id
        receiver = request.data["receiver"]
        text = request.data['text']
        group_name = f"{receiver}"
        is_online=redis_conn.get(f"{receiver}_is_online")
        if is_online is  None:
            redis_conn.hsetnx(f'{receiver}_messages', str(uuid.uuid4()), str({"text": text ,"sender":user,"receiver":receiver}))
            
        

        #try:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'chat_message',
                'message': json.dumps({'sender': user, 'receiver': receiver, 'text': text})
            }
        )
    
        #except:
        #    return Response({'conflict': 'try again!!'}, status=status.HTTP_409_CONFLICT)    


        #try:
        Message.objects.create(
            sender=User.objects.get(id=user), 
            receiver=User.objects.get(id=receiver),
            text=text,


        )


        # except:
        #      return Response({'conflict': 'try again!!'}, status=status.HTTP_409_CONFLICT)

        return Response(" text sent", status=status.HTTP_200_OK)



class MyChatsView(APIView):
    permission_classes = (IsAuthenticated, ) 
    def get(self, request):
        people=[]
        user = request.user.id

        message=Message.objects.filter(Q(receiver=user) | Q(sender=user)   ).values_list('sender', 'receiver').order_by('-created')
        for friend in message:
            people.extend(friend)
        people=set(people)
        people.remove(user)
        return Response(people)



class MyMessagesView(APIView):
    permission_classes = (IsAuthenticated, ) 
    def get(self, request,pk):
        
        user = request.user.id
        
        if user == pk :
            return Response({'receiver and sender': 'you cant pm your self'}, status=status.HTTP_400_BAD_REQUEST)      


        message=Message.objects.filter(Q(receiver=user , sender=pk) | Q(sender=user,receiver=pk)   ).order_by('created')
        srz=MessageSerializer(message,many=True)
        return Response(srz.data)


class GetUserNotifications(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        notifications = Notifications.objects.filter(receiver = request.user.id).order_by('-created')
        serializer = NotificationSerializer(notifications, many = True)
        return Response(data = {"data sended"}, status = status.HTTP_200_OK)



# delete a message 
class DeleteMessageView(APIView):
    permission_classes = (IsAuthenticated, )

    def delete(self, request):
        if (not "message_id" in request.data) :
            return Response({'message_id': 'message_id is required'}, status=status.HTTP_400_BAD_REQUEST)           
        message_id = request.data["message_id"]
        try:
            message = Message.objects.get(id=message_id)
            message.delete()
            return Response("message deleted", status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'conflict': 'some problem in your request'}, status=status.HTTP_409_CONFLICT)





# delete a chat
class DeleteChatView(APIView):
    permission_classes = (IsAuthenticated, )

    def delete(self, request):
        if (not "user_id" in request.data) :
            return Response({'user_id': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # delete all messages between request.user and user_id
        user_id = request.data["user_id"]
        try:
            messages = Message.objects.filter(Q(sender=request.user.id, receiver=user_id) | Q(sender=user_id, receiver=request.user.id))
            messages.delete()
            return Response("message deleted", status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'conflict': 'some problem in your request'}, status=status.HTTP_409_CONFLICT)


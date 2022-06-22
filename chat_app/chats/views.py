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
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'chat_message',
                    'message': json.dumps({'sender': user, 'receiver': receiver, 'text': text})
                }
            )
        except:
            return Response({'conflict': 'try again!!'}, status=status.HTTP_409_CONFLICT)    


        try:
            Message.objects.create(
                sender=User.objects.get(id=user), 
                receiver=User.objects.get(id=receiver),
                text=text,


            )


        except:
             return Response({'conflict': 'try again!!'}, status=status.HTTP_409_CONFLICT)

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
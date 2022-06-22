from rest_framework import serializers
from .models import Message, Notifications


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('__all__')



class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ('__all__')
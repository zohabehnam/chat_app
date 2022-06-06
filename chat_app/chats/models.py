from django.db import models
from accounts.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sender", on_delete = models.CASCADE)
    receiver = models.ForeignKey(User,related_name="receiver", on_delete = models.CASCADE)
    text = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)



class Notifications(models.Model):
    sender = models.ForeignKey(User,related_name="sender_notif" ,on_delete=models.CASCADE)
    receiver = models.ForeignKey(User,related_name="receiver_notif", on_delete=models.CASCADE)
    action_type = models.CharField(max_length=50)



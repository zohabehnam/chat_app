from django.contrib import admin
from .models import Message, Notifications
# Register your models here.


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver',"text")

@admin.register(Notifications)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver',"type")
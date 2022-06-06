from django.contrib import admin
from .models import Message, Notifications


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver',"text")

@admin.register(Notifications)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver',"action_type")
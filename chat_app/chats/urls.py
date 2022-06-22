from django.urls import path
from . views import NewMessage,MyChatsView,MyMessagesView

urlpatterns = [
    path('',NewMessage.as_view(),name="chat" ),
    path('chats/',MyChatsView.as_view(),name="chat"),
    path('messages/<int:pk>/',MyMessagesView.as_view(),name="messages")


]
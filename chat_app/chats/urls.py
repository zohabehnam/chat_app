from django.urls import path
from . views import NewMessage, MyChatsView, MyMessagesView, DeleteChatView, DeleteMessageView

urlpatterns = [
    path('',NewMessage.as_view(),name="chat" ),
    path('chats/',MyChatsView.as_view(),name="chat"),
    path('messages/<int:pk>/',MyMessagesView.as_view(),name="messages"),
    path('delete_chat/',DeleteChatView.as_view(),name="delete_chat"),
    path('delete_message/',DeleteMessageView.as_view(),name="delete_message"),

]
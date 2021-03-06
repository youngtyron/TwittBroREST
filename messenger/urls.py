from django.urls import path
from messenger.views import *


urlpatterns = [
    path('chats/', ChatListView.as_view()),
    path('chat/<int:chat_id>/', DialogueView.as_view()),
    path('write/<int:user_id>/', WriteMessageView.as_view()),
    path('read/<int:chat_id>/', ReadView.as_view()),
    path('new/', NewMessagesView.as_view()),
    path('unread/', NewUnreadView.as_view()),
    path('get_chats_to_add_user/<int:user_id>/', AddUserToChatView.as_view()),
    path('createchat/', CreateChat.as_view()),
]

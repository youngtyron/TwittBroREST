from django.urls import path
from messenger.views import *
# from .views import [PostsView, DeletePostView, LikeView, SearchView, UserView, FollowView, NewsView, UserNewsView, AvatarView, AvatarNewsView,
#                    FollowingsView]

urlpatterns = [
    path('chats/', ChatListView.as_view()),
    path('chat/<int:chat_id>/', DialogueView.as_view()),
    path('write/<int:user_id>/', WriteMessageView.as_view()),
    path('read/<int:chat_id>/', ReadView.as_view()),
    path('new/<int:chat_id>/', NewMessagesView.as_view()),
    path('unread/', NewUnreadView.as_view()),
    path('get_chats_to_add_user/<int:user_id>/', AddUserToChatView.as_view()),
    path('createchat/', CreateChat.as_view()),
]

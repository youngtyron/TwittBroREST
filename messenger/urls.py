from django.urls import path
from messenger.views import *
# from .views import [PostsView, DeletePostView, LikeView, SearchView, UserView, FollowView, NewsView, UserNewsView, AvatarView, AvatarNewsView,
#                    FollowingsView]

urlpatterns = [
    path('chats/', ChatListView.as_view()),
    path('chat/<int:chat_id>/', DialogueView.as_view()),
    path('read/<int:chat_id>/', ReadView.as_view()),
]

from django.urls import path
from profiles.views import *
# from .views import [PostsView, DeletePostView, LikeView, SearchView, UserView, FollowView, NewsView, UserNewsView, AvatarView, AvatarNewsView,
#                    FollowingsView]

urlpatterns = [
    path('posts/<int:user_id>/', PostsView.as_view()),
    path('delete_post/<int:user_id>/', DeletePostView.as_view()),
    path('load_results/', SearchView.as_view()),
    path('like_post/', LikeView.as_view()),
    path('user/<int:user_id>/', UserView.as_view()),
    path('follow/<int:user_id>/', FollowView.as_view()),
    path('news/', NewsView.as_view()),
    path('user_news/', UserNewsView.as_view()),
    path('avatar/<int:user_id>/', AvatarView.as_view()),
    path('avatarnews/', AvatarNewsView.as_view()),
    path('followings/', FollowingsView.as_view()),
]

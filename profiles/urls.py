from django.urls import path
from .views import PostsView, DeletePostView, LikeView

urlpatterns = [
    path('posts/<int:user_id>/', PostsView.as_view()),
    path('delete_post/<int:user_id>/', DeletePostView.as_view()),
    path('like_post/', LikeView.as_view()),


]

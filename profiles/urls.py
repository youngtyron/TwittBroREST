from django.urls import path
from .views import PostsView

urlpatterns = [
    path('posts/<int:user_id>/', PostsView.as_view()),

]

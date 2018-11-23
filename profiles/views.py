from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User
from profiles.models import Post
from profiles.serializers import PostSerializer
from twittbro.myfunctions import its_empty_string

class PostsView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, user_id):
        user = User.objects.get(id = user_id)
        posts = Post.objects.filter(author = user)
        serializer = PostSerializer(posts, many=True)
        return Response({"data": serializer.data})

    def post(self, request, user_id):
        user = User.objects.get(id = user_id)
        if request.user == user:
            text = request.POST.get('text')
            if its_empty_string(text):
                return Response(status=400, data={'empty':True})
            else:
                Post.objects.create(author = request.user, text = text)
                return Response(status=201)
        else:
            return Response(status=400)

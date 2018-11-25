from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User
from profiles.models import Post, Like
from profiles.serializers import PostSerializer
from twittbro.myfunctions import its_empty_string

class PostsView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, user_id):
        counter = int(request.GET.get('id'))
        print(counter)
        user = User.objects.get(id = user_id)
        posts = Post.objects.filter(author = user)
        portion_posts = posts.values_list('pk', flat=True)[counter:counter+10]
        posts = Post.objects.filter(pk__in = portion_posts)
        serializer = PostSerializer(posts, many=True)
        i = 0
        while i < posts.count():
            post = posts.get(id = serializer.data[i]['id'])
            if post.user_can_likes(request.user):
                serializer.data[i].update({'red': False})
            else:
                serializer.data[i].update({'red': True})
            i = i+1
        if user == request.user:
            return Response({"data": serializer.data, 'mywall':True})
        else:
            return Response({"data": serializer.data})

    def post(self, request, user_id):
        user = User.objects.get(id = user_id)
        if request.user == user:
            text = request.POST.get('text')
            if its_empty_string(text):
                return Response(status=400, data={'empty':True})
            else:
                post = Post.objects.create(author = request.user, text = text)
                serializer = PostSerializer(post)
                return Response({"data": serializer.data})
        else:
            return Response(status=400)

class DeletePostView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]


    def post(self, request, user_id):
        user = User.objects.get(id = user_id)
        if request.user == user:
            post = Post.objects.get(id = request.POST.get('id'))
            post.delete()
            return Response(status=201)
        else:
            return Response(status=400)

class LikeView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        post = Post.objects.get(id = request.POST.get('id'))
        if post.user_can_likes(request.user):
            post.like(request.user)
            return Response(status=201, data={'red':True, 'likes':post.likes_quanity})
        else:
            post.unlike(request.user)
            return Response(status=201, data={'white':True, 'likes':post.likes_quanity})

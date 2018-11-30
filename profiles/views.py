from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User
from profiles.models import Post, Like, Following, Profile
from profiles.serializers import PostSerializer, UserSerializer, ProfileSerializer
from twittbro.myfunctions import its_empty_string
from django.shortcuts import get_object_or_404



class UserNewsView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({"data": serializer.data})

class NewsView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        counter = int(request.GET.get('last'))

        if counter == 0:
            news = request.user.profile.query_news()
        else:
            news = request.user.profile.query_news_with_counter(counter)
        portion_news = news.values_list('pk', flat=True)[0:10]
        news = Post.objects.filter(pk__in = portion_news)
        serializer = PostSerializer(news, many=True)
        i = 0
        while i < news.count():
            post = news.get(id = serializer.data[i]['id'])
            if post.user_can_likes(request.user):
                serializer.data[i].update({'red': False})
            else:
                serializer.data[i].update({'red': True})
            i = i+1
        return Response({"data": serializer.data})


class FollowingsView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        followings = Following.objects.filter(who=request.user)
        users = []
        for f in followings:
            users.append(f.to)
        serializer = UserSerializer(users, many=True)

        i = 0
        while i < len(users):
            user = users[i]
            if user.profile.avatar and hasattr(user.profile.avatar, 'url'):
                url = '/static' + str(user.profile.avatar.url)
                serializer.data[i].update({'ava': url})
            else:
                serializer.data[i].update({'ava': False})
            i = i+1
        return Response({"data": serializer.data})

class FollowView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, user_id):
        followed = get_object_or_404(User, id = user_id)
        following = Following.objects.filter(who = request.user, to = followed)
        if not following.exists():
            Following.objects.create(who = request.user, to = followed)
            followed.profile.rating = followed.profile.rating + 1
            followed.profile.save()
            return Response(status=201, data={'create_follow':True})
        else:
            followed.profile.rating = followed.profile.rating - 1
            followed.profile.save()
            following.delete()
            return Response(status=201, data={'delete_follow':True})


class UserView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, user_id):
        user = User.objects.get(id = user_id)
        serializer = UserSerializer(user)
        following = Following.objects.filter(who = request.user, to = user)
        if following.exists():
            return Response({"data": serializer.data, 'you_follow': True})
        else:
            return Response({"data": serializer.data})


class AvatarView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, user_id):
        user = User.objects.get(id = user_id)
        if user.profile.avatar and hasattr(user.profile.avatar, 'url'):
            return Response({"data": user.profile.avatar.url})
        else:
            return Response(status=400)

class AvatarNewsView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        if request.user.profile.avatar and hasattr(request.user.profile.avatar, 'url'):
            return Response({"data": request.user.profile.avatar.url})
        else:
            return Response(status=400)

class PostsView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, user_id):
        counter = int(request.GET.get('last'))
        user = User.objects.get(id = user_id)
        if counter == 0:
            posts = Post.objects.filter(author = user)
        else:
            posts = Post.objects.filter(author = user, id__lt=counter)
        portion_posts = posts.values_list('pk', flat=True)[0:10]
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
                return Response(status=201, data={'empty':True})
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

class SearchView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        text = request.GET.get('text')
        #Поиск среди имен
        # name_results = User.objects.filter(Q(first_name__icontains = text) | Q(last_name__icontains=text))
        #Поиск среди текста постов
        results = Post.objects.filter(text__icontains = text)
        portion_res = results.values_list('pk', flat=True)[0:10]
        results = Post.objects.filter(pk__in = portion_res)
        serializer = PostSerializer(results, many=True)
        i = 0
        while i < results.count():
            post = results.get(id = serializer.data[i]['id'])
            if post.user_can_likes(request.user):
                serializer.data[i].update({'red': False})
            else:
                serializer.data[i].update({'red': True})
            i = i+1
        return Response({"data": serializer.data})

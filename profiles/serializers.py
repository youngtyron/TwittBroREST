from rest_framework import serializers
from django.contrib.auth.models import User
from profiles.models import Post


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('author', 'text', 'pub_date', 'id', 'likes_quanity')
        depth = 1

from rest_framework import serializers
from django.contrib.auth.models import User
from profiles.models import Post, Profile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'id')


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('author', 'text', 'pub_date', 'id', 'likes_quanity')
        depth = 1

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('rating', 'avatar')

        # fields = ('rating', 'avatar', 'avatar_profile', 'avatar_mini', 'avatar_micro')

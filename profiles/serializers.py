from rest_framework import serializers
from django.contrib.auth.models import User
from profiles.models import Post, Profile, Comment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'id')


class PostSerializer(serializers.ModelSerializer):

    images_data = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('author', 'text', 'pub_date', 'id', 'likes_quanity', 'images_data')
        depth = 1

    def get_images_data(self, obj):
        return self.context.get('images_data')

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('rating', 'avatar')

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        depth = 1

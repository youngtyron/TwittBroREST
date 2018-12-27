from rest_framework import serializers
from django.contrib.auth.models import User
from profiles.models import Post, Profile, Comment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'id')

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance

class PostSerializer(serializers.ModelSerializer):

    images_data = serializers.SerializerMethodField()
    small_ava = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    can_repost = serializers.SerializerMethodField()
    pub_date = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('author', 'text', 'id', 'likes_quanity', 'small_ava', 'comments', 'can_repost', 'repost', 'is_repost', 'images_data', 'pub_date')
        depth = 1

    def get_images_data(self, obj):
        return obj.images_urls()

    def get_small_ava(self, obj):
        return obj.author.profile.small_avatar_url()

    def get_comments(self, obj):
        if obj.is_commented():
            return True
        else:
            return False

    def get_can_repost(self, obj):
        return self.context.get('can_repost')

    def get_pub_date(self, obj):
        return obj.pub_date.date()

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('rating', 'avatar')

class CommentSerializer(serializers.ModelSerializer):

    images_data = serializers.SerializerMethodField()
    ultra_avatar = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        depth = 1

    def get_images_data(self, obj):
        return obj.images_urls()

    def get_ultra_avatar(self, obj):
        ultra_avatar = obj.commentator.profile.ultra_avatar_url()
        return ultra_avatar
        # return self.context.get('commentator_ultra_avatar')

from rest_framework import serializers
from django.contrib.auth.models import User
from messenger.models import Chat, Message
from profiles.serializers import UserSerializer


class ChatSerializer(serializers.ModelSerializer):

    new = serializers.SerializerMethodField()
    chat_name = serializers.SerializerMethodField()


    class Meta:
        model = Chat
        fields = ('name', 'members', 'is_group', 'id', 'new', 'chat_name')
        depth = 1

    def get_new(self, obj):
        return self.context.get('new')

    def get_chat_name(self, obj):
        return self.context.get('chat_name')

class MessagesSerializer(serializers.ModelSerializer):

    grey = serializers.SerializerMethodField()
    my_grey = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ('writer', 'text', 'pub_date', 'is_read', 'who_read', 'id', 'chat', 'grey', 'my_grey')
        depth = 1

    def get_grey(self, obj):
        return self.context.get('grey')

    def get_my_grey(self, obj):
        return self.context.get('my_grey')

from rest_framework import serializers
from django.contrib.auth.models import User
from messenger.models import Chat, Message


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ('name', 'members', 'is_group', 'id')
        depth = 1

class MessagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('writer', 'text', 'pub_date', 'is_read', 'who_read')
        depth = 1

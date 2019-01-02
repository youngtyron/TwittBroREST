from rest_framework import serializers
from django.contrib.auth.models import User
from messenger.models import Chat, Message
from profiles.serializers import UserSerializer
import datetime


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

    images_data = serializers.SerializerMethodField()
    grey = serializers.SerializerMethodField()
    my_grey = serializers.SerializerMethodField()
    pub_date = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ('writer', 'text', 'pub_date', 'is_read', 'who_read', 'id', 'chat', 'grey', 'my_grey', 'images_data')
        depth = 1

    def get_grey(self, obj):
        return self.context.get('grey')

    def get_my_grey(self, obj):
        return self.context.get('my_grey')

    def get_images_data(self, obj):
        return obj.images_urls()

    def get_pub_date(self, obj):
        today = datetime.datetime.today()
        if obj.pub_date.date() < today.date():
            return obj.pub_date.date()
        else:
            return obj.pub_date.time().strftime("%H-%M")

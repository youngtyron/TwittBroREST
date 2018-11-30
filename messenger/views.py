from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User
from messenger.models import Chat, Message
from messenger.serializers import ChatSerializer, MessagesSerializer
from twittbro.myfunctions import its_empty_string


class ChatListView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        chats = request.user.chats.all()
        serializer = ChatSerializer(chats, many=True)
        return Response({'data': serializer.data})

class DialogueView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, chat_id):
        chat = Chat.objects.get(id = chat_id)
        if chat in request.user.chats.all():
            messages = chat.messages.all()
            serializer = MessagesSerializer(messages, many=True)
            return Response({'data': serializer.data})
        else:
            return Response(status=400)

    def post(self, request, chat_id):
        chat = Chat.objects.get(id = chat_id)
        if chat in request.user.chats.all():
            text = request.POST.get('text')
            if its_empty_string(text):
                return Response(status=201, data={'empty':True})
            else:
                message = Message.objects.create(writer = request.user, text=text, chat=chat)
                message.who_read.add(request.user)
                serializer = MessagesSerializer(message)
                return Response({"data": serializer.data})
        else:
            return Response(status=400)

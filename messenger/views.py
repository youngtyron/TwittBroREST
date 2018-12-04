from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User
from messenger.models import Chat, Message
from messenger.serializers import ChatSerializer, MessagesSerializer
from twittbro.myfunctions import its_empty_string


class NewMessagesView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, chat_id):
        newest = request.GET.get('newest')
        chat = Chat.objects.get(id = chat_id)
        if chat in request.user.chats.all():
            messages = chat.query_newer_messages(newest)
            if messages.exists():
                serializer = MessagesSerializer(messages, many=True)
                return Response({'data': serializer.data})
            else:
                return Response(status = 201, data = {'not_new': True})
        else:
            return Response(status=400)

class ReadView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, chat_id):
        chat = Chat.objects.get(id = chat_id)
        if chat in request.user.chats.all():
            ids = list(dict(request.POST).values())[0]
            white = []
            for id in ids:
                message = Message.objects.get(id = id)
                message.who_read.add(request.user)
                message.checking_on_read()
                if not message.is_grey_for_me(request.user):
                    white.append(message.id)
            return Response(status=201, data={'white': white})
        else:
            return Response(status=400)


class ChatListView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        chats = request.user.chats.all()
        serializer = ChatSerializer(chats, many=True)
        i = 0
        while i < chats.count():
            chat = chats.get(id = serializer.data[i]['id'])
            serializer.data[i].update({'new': chat.count_new_messages(request.user)})
            i = i+1
        return Response({'data': serializer.data})

class DialogueView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, chat_id):
        chat = Chat.objects.get(id = chat_id)
        if chat in request.user.chats.all():
            counter = int(request.GET.get('last'))
            if counter == 0:
                messages = chat.query_messages()
            else:
                messages = chat.query_messages_with_counter(counter)
            portion_messages = messages.values_list('pk', flat=True)[0:10]
            messages = Message.objects.filter(pk__in = portion_messages)
            serializer = MessagesSerializer(messages, many=True)
            i = 0
            while i < messages.count():
                message = messages.get(id = serializer.data[i]['id'])
                if message.is_grey(request.user):
                    serializer.data[i].update({'grey': True})
                if message.is_grey_for_me(request.user):
                    serializer.data[i].update({'my_grey': True})
                i = i+1
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
                serializer = MessagesSerializer(message, context={'grey': True})
                return Response({"data": serializer.data})
        else:
            return Response(status=400)

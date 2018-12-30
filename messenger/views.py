from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User
from messenger.models import Chat, Message, ImageMessage
from messenger.serializers import ChatSerializer, MessagesSerializer
from twittbro.myfunctions import its_empty_string
from profiles.serializers import UserSerializer


class CreateChat(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        followings = request.user.followings.all()
        followers = request.user.followers.all()
        people = []
        for f in followings:
            people.append(f.to)
        for f in followers:
            people.append(f.who)
        people = list(set(people))
        serializer = UserSerializer(people, many=True)
        return Response({'data': serializer.data})

    def  post(self, request):
        ids = list(dict(request.POST).values())[0]
        print(ids)
        users = []
        for id in ids:
            user = User.objects.get(id = id)
            users.append(user)
        chat = Chat.objects.create(is_group = True)
        chat.members.add(request.user)
        for user in users:
            chat.members.add(user)
        return Response(status = 201)

class AddUserToChatView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, user_id):
        user = User.objects.get(id= user_id)
        chats = Chat.objects.filter(members = request.user, is_group=True).exclude(members = user)
        serializer = ChatSerializer(chats, many=True)
        i=0
        while i < chats.count():
            chat = chats.get(id = serializer.data[i]['id'])
            companions= chat.companions(request.user)
            miniselializer = UserSerializer(companions, many=True)
            serializer.data[i].update({'chat_name': miniselializer.data})
            i = i+1
        return Response({'data': serializer.data})

    def post(self, request, user_id):
        chat = Chat.objects.get(id = request.POST.get('chat'))
        user = User.objects.get(id = user_id)
        chat.members.add(user)
        chat.save()
        return Response(status=201)


class NewUnreadView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        # chats = request.user.chats.all()
        # counter = 0
        # for chat in chats:
        #     counter = counter + chat.count_new_messages(request.user)
        counter = request.user.profile.home_unread_messages()
        return Response({'data': counter})

class WriteMessageView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, user_id):
        user = User.objects.get(id= user_id)
        text =  request.POST.get('text')
        if its_empty_string(text):
            return Response(status=400, data={'empty':True})
        else:
            chat = Chat.objects.filter(members = user, is_group=False).filter(members = request.user)
            if chat.exists():
                chat = chat[0]
                message = Message.objects.create(chat = chat, text = text, writer = request.user)
                message.who_read.add(request.user)
                message.save()
            else:
                chat = Chat.objects.create(is_group=False)
                chat.members.add(request.user)
                chat.members.add(user)
                chat.save()
                message = Message.objects.create(chat = chat, text = text, writer = request.user)
                message.who_read.add(request.user)
                message.save()
            return Response(status = 201)


class NewMessagesView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        newest = request.GET.get('newest')
        id = request.GET.get('id')
        chat = Chat.objects.get(id = id)
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
                message.save()
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
            companions= chat.companions(request.user)
            miniselializer = UserSerializer(companions, many=True)
            serializer.data[i].update({'chat_name': miniselializer.data})
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
            companions= chat.companions(request.user)
            miniselializer = UserSerializer(companions, many=True)
            chatserializer = ChatSerializer(chat, context={'chat_name': miniselializer.data})
            i = 0
            while i < messages.count():
                message = messages.get(id = serializer.data[i]['id'])
                if message.is_grey(request.user):
                    serializer.data[i].update({'grey': True})
                if message.is_grey_for_me(request.user):
                    serializer.data[i].update({'my_grey': True})
                i = i+1
            return Response({'data': serializer.data, 'chatdata': chatserializer.data})
        else:
            return Response(status=400)

    def post(self, request, chat_id):
        chat = Chat.objects.get(id = chat_id)
        if chat in request.user.chats.all():
            text = request.POST.get('text')
            images = request.FILES.getlist('messageimages')
            if images:
                message = Message.objects.create(writer = request.user, chat=chat)
                for image in images:
                    imagemessage = ImageMessage.objects.create(message = message, image = image)
                if text:
                    if not its_empty_string(text):
                        message.text = text
                        message.save()
                        serializer = MessagesSerializer(message)
                        return Response({"data": serializer.data})
                else:
                    serializer = MessagesSerializer(message)
                    return Response({"data": serializer.data})
            else:
                if its_empty_string(text):
                    return Response(status=201, data={'empty':True})
                else:
                    message = Message.objects.create(writer = request.user, text=text, chat=chat)
                    message.who_read.add(request.user)
                    message.save()
                    serializer = MessagesSerializer(message, context={'grey': True})
                    return Response({"data": serializer.data})
        else:
            return Response(status=400)

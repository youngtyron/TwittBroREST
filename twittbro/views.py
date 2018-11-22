from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User
from profiles.models import Profile
from profiles.serializers import UserSerializer


class RegisterView(APIView):

    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        if request.data.get('password') != request.data.get('confirm_password'):
            return Response(status=400, data={'pass_error':True})
        user = UserSerializer(data=request.data)
        if user.is_valid():
            user = user.save()
            Profile.objects.create(user=request.user)
            return Response(status=201)
        else:
            return Response(status=400)

class GetIdView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        id = request.user.id
        return Response({'id':id})

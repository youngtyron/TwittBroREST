from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User
from profiles.models import Profile
from profiles.serializers import RegisterSerializer
# from rest_framework.parsers import JSONParser
# from django.contrib.auth.hashers import make_password


class RegisterView(APIView):

    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        if request.POST.get('password') != request.POST.get('confirm_password'):
            return Response(status=400, data={'pass_error':True})
        else:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                user.set_password(request.POST.get('password'))
                user.save()
                Profile.objects.create(user=user)
                return Response(status=201)
            else:
                return Response(status=400)

class GetIdView(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        id = request.user.id
        return Response({'id':id})

from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer,RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics

from django.conf import settings
from django.core.files.storage import default_storage
from joblib import load


# Class based view to Get User Details using Token Authentication
class UserDetailAPI(APIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (AllowAny,)
  def get(self,request,*args,**kwargs):
    user = User.objects.get(id=request.user.id)
    serializer = UserSerializer(user)
    return Response(serializer.data)

#Class based view to register user
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from rest_framework import status

class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            # Authenticate user
            user = authenticate(username=serializer.data['username'],
                                password=request.data['password'])
            if user is not None:
                login(request, user)
                return redirect('/conversation-page/')  
            else:
                return Response({'message': 'Failed to authenticate user.'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response

class ConversationAPIView(APIView):
    def get(self, request):
        
        conversation_data = {...}  
        return Response({'message': 'Welcome to the conversation page!'})
    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from .serializers import LoginSerializer

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                redirect_url = '/conversation-page/'  # Modify this to your desired URL
                return Response({'redirect_url': redirect_url}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

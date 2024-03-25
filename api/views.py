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
class RegisterUserAPIView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer


#getting the model file path using Django storage system
  
def get_model_path():
    model_filename = 'your_model.pkl'  
    return settings.MEDIA_ROOT / model_filename

from rest_framework.views import APIView
from rest_framework import status 
from rest_framework.response import Response
from .serializers import ChatbotInputSerializer, ChatbotOutputSerializer

class ChatbotAPI(APIView):
    serializer_class = ChatbotInputSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_message = serializer.validated_data['user_message']

            # Preprocess user message (if needed)

            # Securely load the model from storage
            model_path = get_model_path()
            if default_storage.exists(model_path):
                with default_storage.open(model_path, 'rb') as f:
                    chatbot_model = load(f)
            else:
                return Response({'error': 'Model file not found'}, status=status.HTTP_404_NOT_FOUND)

            # Get response from the loaded model
            bot_response = chatbot_model.predict(user_message)  # Adapt for your framework

            # Postprocess bot response (if needed)

            serializer = ChatbotOutputSerializer({'bot_response': bot_response})
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


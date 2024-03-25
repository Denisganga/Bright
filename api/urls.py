from django.urls import path
from .views import UserDetailAPI,RegisterUserAPIView,ChatbotAPI
urlpatterns = [
  path("get-details",UserDetailAPI.as_view()),
  path('register',RegisterUserAPIView.as_view()),
  path('chat/', ChatbotAPI.as_view(), name='chatbot_api')
]
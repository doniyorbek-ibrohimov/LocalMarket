from django.urls import path
from .views import RegisterAPIView, UserProfileAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('my-profile/', UserProfileAPIView.as_view()),
]
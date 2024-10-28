
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.LoginAPIView.as_view()),

    path('login/otp/', views.OTPVerificationAPIView.as_view()),
]

from django.contrib.auth import authenticate, login as django_login
from django_otp import login, match_token
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class OTPSerializer(serializers.Serializer):
    otp_token = serializers.CharField(max_length=6)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                django_login(request, user)
                return Response({'detail': 'Login successful. Please verify OTP.'}, status=status.HTTP_200_OK)
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OTPVerificationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OTPSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            otp_token = serializer.validated_data['otp_token']
            verified = match_token(request.user, otp_token)
            if verified:
                login(request, verified)
                return Response({'detail': 'OTP verified successfully'}, status=status.HTTP_200_OK)
            return Response({'detail': 'Invalid OTP Token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

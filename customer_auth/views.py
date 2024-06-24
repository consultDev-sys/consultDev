
from datetime import timedelta
from django.utils import timezone

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError

from customer_auth.api.v1.services.auth_service import generate_otp, send_otp_email
from customer_auth.constants import SENDER_EMAIL
from customer_auth.serializers import CustomUserSerializer


# Registration View
class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        payload = request.data
        serializer = CustomUserSerializer(data=payload)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data        
        otp = generate_otp()
        user_data = {
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'email': data.get('email'),
            'phone_number': data.get('phone_number'),
            'password': make_password(data.get('password')),
            'otp': otp,
            'otp_created_at': timezone.now()
        }
        user = get_user_model().objects.create(**user_data)
        user.save()
        response = send_otp_email(otp, user)
        return Response(response, status=response["code"])
    

# Login View
class LoginUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except TokenError as e:
            return Response(data="Token already blacklisted", status=status.HTTP_400_BAD_REQUEST)
        

class ValidateOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        otp = request.data.get('otp')
        
        user = get_user_model().objects.filter(email=email).first()
        
        if user and user.otp == otp and timezone.now() < user.otp_created_at + timedelta(minutes=10):
            user.email_verified = True
            user.otp = None
            user.otp_created_at = None
            user.save()

            # Generate token for the user
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP or OTP expired'}, status=status.HTTP_400_BAD_REQUEST)

from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError

from consultancy.base_service import BaseService
from customer_auth.api.v1.services.auth_service import generate_otp, login_user, register_user, send_otp_email, validate_otp
from customer_auth.constants import SENDER_EMAIL
from customer_auth.helpers import get_error_string_from_serializer_error_object
from customer_auth.serializers import CustomUserSerializer, LoginSerializer


# Registration View
class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        payload = request.data
        serializer = CustomUserSerializer(data=payload)
        if not serializer.is_valid():
            response = BaseService.send_response(errors=get_error_string_from_serializer_error_object(serializer.errors), 
                                                 code=status.HTTP_400_BAD_REQUEST,
                                                 message="Field not found")
            return Response(response, status=response["code"])
        
        data = serializer.validated_data        
        response = register_user(data)
        return Response(response, status=response["code"])
    

# Login View
class LoginUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            response = BaseService.send_response(errors=get_error_string_from_serializer_error_object(serializer.errors), 
                                                 code=status.HTTP_400_BAD_REQUEST,
                                                 message="Validation error")
            return Response(response, status=response["code"])
        
        data = serializer.validated_data
        response = login_user(request, data["email"], data["password"])
        return Response(response, status=200)


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
        response = validate_otp(email, otp)

        return Response(response, status=response["code"])
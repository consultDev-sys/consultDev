import random
from django.core.mail import send_mail
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from django.contrib.auth import authenticate

from consultancy.base_service import BaseService
from consultancy.settings import DEFAULT_FROM_EMAIL

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(otp, user):
    try:
        send_mail(
                'Thank you for choosing Emirates Launch. We are glad to onboard you with us.',
                f'Your OTP code for registration is {otp}. Please do not share this with anyone. Happy Consulting!!',
                DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        return BaseService.send_response(code=status.HTTP_201_CREATED, data=otp, message="Successfully created")
    except Exception as e:
        return BaseService.send_response(code=status.HTTP_201_CREATED, data=otp, message="Successfully created")
    

def register_user(data):
    try:
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
    except Exception as e:
        response = BaseService.send_response(code=status.HTTP_400_BAD_REQUEST, errors=str(e), message="Bad Request")


def validate_otp(email, otp):
    try:
        user = get_user_model().objects.filter(email=email).first()
        if user and user.otp == otp and timezone.now() < user.otp_created_at + timedelta(minutes=10):
            user.email_verified = True
            user.otp = None
            user.otp_created_at = None
            user.save()

            # Generate token for the user
            refresh = RefreshToken.for_user(user)
            return BaseService.send_response(code=status.HTTP_200_OK, data={'access': str(refresh.access_token)}, message="Validation successful")
        else:
            return BaseService.send_response(code=status.HTTP_400_BAD_REQUEST, message="The OTP you entered is either wrong or expired. Try again")
    except Exception as e:
        return BaseService.send_response(code=status.HTTP_500_INTERNAL_SERVER_ERROR, errors=str(e))
    

def login_user(request, email, password):
    user = authenticate(request, email=email, password=password)
        
    if user is not None:
        refresh = RefreshToken.for_user(user)
        # return BaseService.send_response(code=status.HTTP_200_OK, data={
        #     'access': str(refresh.access_token)
        # }, message="Login Successful")
        return {
            'access': str(refresh.access_token)
        }
    else:
        return BaseService.send_response(code=status.HTTP_401_UNAUTHORIZED, errors='Invalid credentials', message="Invalid credentials")
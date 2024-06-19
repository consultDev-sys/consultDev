import random
from django.core.mail import send_mail
from rest_framework import status

from consultancy.base_service import BaseService
from consultancy.settings import EMAIL_HOST_USER

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(otp, user):
    try:
        send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
        return BaseService.send_response(code=status.HTTP_201_CREATED, message="Successfully created")
    except Exception as e:
        return BaseService.send_response(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Internal Server Error")
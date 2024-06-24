import random
from django.core.mail import send_mail
from rest_framework import status

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
        return BaseService.send_response(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Internal Server Error")
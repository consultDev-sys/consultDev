from django.urls import path
from .views import LogoutView, RegisterUserView, LoginUserView, ValidateOTPView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('validate-otp/', ValidateOTPView.as_view(), name='validate_otp'),  
]

app_name = "auth"
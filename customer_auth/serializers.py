from rest_framework import serializers

from customer_auth.models import Customer

class CustomUserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, obj):
        email_already_exists = Customer.objects.filter(email=obj.get('email'))
        phone_number_exists = Customer.objects.filter(phone_number=obj.get('phone_number'))
        if email_already_exists:
            raise serializers.ValidationError("Email already taken")
        
        if phone_number_exists:
            raise serializers.ValidationError("Phone number already exists")
        
        if obj.get('password') != obj.get('confirm_password'):
            raise serializers.ValidationError("The passwords do not match")
        
        return obj
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
        
        


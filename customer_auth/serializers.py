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
        if email_already_exists:
            raise serializers.ValidationError("Email already taken")
        
        if obj.get('password') != obj.get('confirm_password'):
            raise serializers.ValidationError("The passwords do not match")
        
        return obj
        
        


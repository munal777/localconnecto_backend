from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer

User = get_user_model()

class UserCreationSerializer(RegisterSerializer):
    username = None
    password1 = None
    password2 = None

    password = serializers.CharField(write_only=True)

    def validate(self, validate_data):
        email = validate_data['email']
        password = validate_data['password']

        if not email:
            raise serializers.ValidationError("Email is required to register.")
        
        if not password:
            raise serializers.ValidationError("Password is not provided.")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")

        return validate_data
    
    def get_cleaned_data(self):
        return {
            'email': self.validated_data.get('email', ''),
            'password': self.validated_data.get('password', ''),
        }
    
    def save(self, request):
        clean_data = self.get_cleaned_data()
        
        user = super().save(request)
        user.set_password(clean_data.get('password'))
        user.save()
        return user
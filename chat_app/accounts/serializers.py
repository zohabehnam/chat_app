
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import APIException
from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import ValidationError

from django.contrib.auth import password_validation as validators

from .models import User

class Denied(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = {'error': True, 'message': 'you are not active please activate account or sign up for a new one '}
    
class UserLoginSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        if User.objects.filter(username = attrs['username'], active = False).exists() == True:
            raise Denied
        data = super().validate(attrs)
        return data
    

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'full_name', 'username', 'email', 'password', 'confirm_password'] 
        extra_kwargs = {
            'password': {'write_only': True},
            'is_private': {'read_only': True},
        }

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.pop('confirm_password')
        if password != confirm_password:
            raise ValidationError("passwords do not match")
        try:
            validators.validate_password(data['password'])
        except ValidationError as errors:
            raise errors.messages
        return data

    def create(self, validated_data):
        user = super(UserRegisterSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.active = False
        user.save()
        return user

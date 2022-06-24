from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView,ListAPIView,RetrieveAPIView
from rest_framework import status
from rest_framework.response import Response

from django.conf import settings
from django.core.mail import send_mail

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserLoginSerializer, UserRegisterSerializer
from .models import User
from config.redisConnection import *

import random
import string


class LoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    

class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        if "email" in request.data:
            user = User.objects.filter(email=request.data["email"]).first()
            if user is not None:
                if not user.is_active:
                    user.delete()
        if "username" in request.data:
            user = User.objects.filter(username=request.data["username"]).first()
            if user is not None:
                if not user.is_active:
                    user.delete()

        data = UserRegisterSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        data.save()
        code = ''.join(random.choice(string.digits) for i in range(5))
        is_set = redis_conn.set(code, request.data["email"], 300, nx=True)
        if is_set:
            #subject = 'verification code for chat app'
            #message = code
            #email_from = settings.EMAIL_HOST_USER
            #recipient_list = [request.data['email'],]
            #send_mail( subject, message, email_from, recipient_list, fail_silently=False)
            print(code)
            return Response(data.data, status=status.HTTP_200_OK)
        return Response(data = {"security conflict"}, status=status.HTTP_400_BAD_REQUEST)
        
    

class VerifyEmailView(APIView): 
    permission_classes = [permissions.AllowAny]

    def post(self, request):

        if 'code' in request.data:
            code = request.data['code']
            validation_code = redis_conn.get(code)
            if validation_code is not None:
                email = validation_code
                user = User.objects.get(email=email)
                if user is not None:
                    refresh = RefreshToken.for_user(user)
                    user.active = True
                    user.save()
                    data = {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'message': "email verified successfully",
                    }
                    redis_conn.delete(code)
                    return Response(data=data, status=status.HTTP_200_OK)
                return Response(data={"invalid code"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(data={"invalid code"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"field code is required"}, status=status.HTTP_400_BAD_REQUEST)

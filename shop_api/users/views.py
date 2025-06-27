from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import UserCreateSerializer, UserAuthSerializer, UserConfirmSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import random
from .models import ConfirmationCode
from rest_framework.permissions import AllowAny




class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        user = User.objects.create_user(
            username=username,
            password=password,
            is_active=False
        )


        code = f"{random.randint(100000, 999999)}"
        ConfirmationCode.objects.create(user=user, code=code)
        return Response(status=status.HTTP_201_CREATED,
                        data={'user_id': user.id, 'confirmation_code': code})


class AuthorizationAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED)



class ConfirmUserAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        code = serializer.validated_data['code']
        try:
            user = User.objects.get(username=username)
            confirmation = ConfirmationCode.objects.get(user=user)
        except (User.DoesNotExist, ConfirmationCode.DoesNotExist):
            return Response(status=400, data={"error": "invalid user or cod"})
        if confirmation.code == code:
            user.is_active = True
            user.save()
            confirmation.delete()
            return Response(data={"message": "user confirmed successfully"})
        return Response(status=400, data={"error": "incorrect code"})

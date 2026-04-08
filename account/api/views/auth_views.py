from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from account.api.serializers.auth_serializer import LoginSerializer
from account.api.serializers.user_serializer import RegisterSerializer


# 🔐 LOGIN
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            refresh = RefreshToken.for_user(user)

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# REGISTER
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
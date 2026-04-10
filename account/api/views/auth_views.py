from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from drf_spectacular.utils import extend_schema, OpenApiResponse  # ← Import indispensable

from account.api.serializers.auth_serializer import LoginSerializer
from account.api.serializers.user_serializer import RegisterSerializer


# 🔐 LOGIN
class LoginView(APIView):
    @extend_schema(
        request=LoginSerializer,   # ← Le sérializer utilisé pour la requête POST
        responses={
            200: OpenApiResponse(description="Connexion réussie, tokens JWT retournés"),
            400: OpenApiResponse(description="Identifiants invalides"),
        }
    )
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
    # Pas besoin d'annotation supplémentaire car CreateAPIView est automatiquement documenté
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.permissions import AllowAny  # ← Crucial pour l'accès public
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiResponse

from account.api.serializers.auth_serializer import LoginSerializer
from account.api.serializers.user_serializer import RegisterSerializer

# 🔐 LOGIN
class LoginView(APIView):
    permission_classes = [AllowAny]  # ← Permet de se connecter sans être déjà authentifié

    @extend_schema(
        request=LoginSerializer,
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
                "user": {
                    "username": user.username,
                    "email": user.email
                }
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 📝 REGISTER
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  # ← Indispensable pour créer un compte sans token

    @extend_schema(
        responses={
            201: OpenApiResponse(description="Utilisateur créé avec succès"),
            400: OpenApiResponse(description="Données invalides (ex: email déjà utilisé)"),
        }
    )
    def post(self, request, *args, **kwargs):
        # On utilise la méthode de CreateAPIView mais on peut la surcharger pour personnaliser la réponse
        return super().post(request, *args, **kwargs)
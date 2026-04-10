from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Importations Swagger
from drf_spectacular.utils import extend_schema, OpenApiResponse

from account.api.serializers.profile_serializer import ProfileSerializer

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        # Sérializer utilisé pour la réponse (GET)
        responses={
            200: ProfileSerializer,
            401: OpenApiResponse(description="Non authentifié"),
        },
        description="Retourne le profil de l'utilisateur connecté"
    )
    def get(self, request):
        serializer = ProfileSerializer(request.user.profile)
        return Response(serializer.data)
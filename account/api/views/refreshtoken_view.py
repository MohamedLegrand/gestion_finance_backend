"""
Vue dédiée au rafraîchissement du token JWT.
Utilise simplejwt pour générer un nouvel access token à partir d'un refresh token valide.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse


class RefreshTokenView(APIView):
    """
    Endpoint pour obtenir un nouvel access token.
    Nécessite un refresh token valide dans le corps de la requête.
    """

    @extend_schema(
        request=TokenRefreshSerializer,
        responses={
            200: OpenApiResponse(
                description="Nouvel access token généré avec succès",
                response=TokenRefreshSerializer
            ),
            401: OpenApiResponse(description="Refresh token invalide ou expiré"),
            400: OpenApiResponse(description="Requête mal formée"),
        },
        description="Envoyez votre refresh token pour recevoir un nouvel access token."
    )
    def post(self, request):
        """
        Traite la demande de rafraîchissement de token.
        """
        serializer = TokenRefreshSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            # En cas d'erreur (token invalide, expiré, ou mal formé)
            return Response(
                {"detail": "Refresh token invalide ou expiré", "error": str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )
        # Retourne le nouvel access token
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema # Pour la documentation
from finances.models.compte_model import Compte
from finances.api.serializers.compte_serializer import (
    CompteSerializer,
    CompteDetailSerializer
)
from finances.services.compte_service import CompteService


class CompteListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CompteSerializer # Pour corriger l'erreur Swagger

    def get(self, request):
        comptes = CompteService.get_comptes_user(request.user)
        serializer = CompteSerializer(
            comptes,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CompteSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompteDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CompteSerializer # Par défaut pour PUT/PATCH

    def get_object(self, request, pk):
        try:
            return Compte.objects.get(id=pk, user=request.user)
        except Compte.DoesNotExist:
            return None

    @extend_schema(responses=CompteDetailSerializer) # Spécifie le serializer de détail
    def get(self, request, pk):
        compte = self.get_object(request, pk)
        if not compte:
            return Response(
                {'error': 'Compte introuvable.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CompteDetailSerializer(
            compte,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        compte = self.get_object(request, pk)
        if not compte:
            return Response(
                {'error': 'Compte introuvable.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CompteSerializer(
            compte,
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        compte = self.get_object(request, pk)
        if not compte:
            return Response(
                {'error': 'Compte introuvable.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CompteSerializer(
            compte,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        compte = self.get_object(request, pk)
        if not compte:
            return Response(
                {'error': 'Compte introuvable.'},
                status=status.HTTP_404_NOT_FOUND
            )
        # Bonne pratique : On utilise la méthode du service pour désactiver
        CompteService.desactiver_compte(compte)
        return Response(
            {'message': 'Compte désactivé avec succès.'},
            status=status.HTTP_204_NO_CONTENT
        )


class CompteSoldeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: dict})
    def get(self, request):
        solde_total = CompteService.get_solde_total(request.user)
        comptes = CompteService.get_comptes_user(request.user)
        serializer = CompteSerializer(
            comptes,
            many=True,
            context={'request': request}
        )
        return Response({
            'solde_total': solde_total,
            'comptes': serializer.data
        }, status=status.HTTP_200_OK)
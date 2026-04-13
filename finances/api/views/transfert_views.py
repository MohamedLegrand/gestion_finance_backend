from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter # Pour la doc
from finances.api.serializers.transfert_serializer import TransfertSerializer
from finances.services.transfert_service import TransfertService


class TransfertListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransfertSerializer # Correction Swagger

    @extend_schema(
        parameters=[
            OpenApiParameter(name='compte_source_id', description='ID du compte source', required=False, type=int),
            OpenApiParameter(name='compte_destination_id', description='ID du compte destination', required=False, type=int),
            OpenApiParameter(name='mois', description='Mois (1-12)', required=False, type=int),
            OpenApiParameter(name='annee', description='Année', required=False, type=int),
        ]
    )
    def get(self, request):
        filters = {
            'compte_source_id': request.query_params.get('compte_source_id'),
            'compte_destination_id': request.query_params.get('compte_destination_id'),
            'mois': request.query_params.get('mois'),
            'annee': request.query_params.get('annee'),
        }
        filters = {k: v for k, v in filters.items() if v is not None}

        transferts = TransfertService.get_transferts_user(
            request.user,
            filters=filters
        )
        serializer = TransfertSerializer(
            transferts,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TransfertSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransfertDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransfertSerializer

    def get_object(self, request, pk):
        return TransfertService.get_transfert_by_id(request.user, pk)

    def get(self, request, pk):
        transfert = self.get_object(request, pk)
        if not transfert:
            return Response(
                {'error': 'Transfert introuvable.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = TransfertSerializer(
            transfert,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        transfert = self.get_object(request, pk)
        if not transfert:
            return Response(
                {'error': 'Transfert introuvable.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # L'annulation via le service s'occupe de remettre les soldes à jour
        TransfertService.annuler_transfert(transfert)
        return Response(
            {'message': 'Transfert annulé avec succès.'},
            status=status.HTTP_204_NO_CONTENT
        )
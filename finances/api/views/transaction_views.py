from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter # Pour la documentation
from finances.models.transaction_model import Transaction
from finances.api.serializers.transaction_serializer import (
    TransactionListSerializer,
    TransactionDetailSerializer
)
from finances.services.transaction_service import TransactionService
from finances.utils.calculators import FinanceCalculator


class TransactionListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionDetailSerializer # Sérialiseur par défaut (pour le POST)

    @extend_schema(
        parameters=[
            OpenApiParameter(name='compte_id', description='ID du compte', required=False, type=int),
            OpenApiParameter(name='categorie_id', description='ID de la catégorie', required=False, type=int),
            OpenApiParameter(name='type', description='depense ou revenu', required=False, type=str),
            OpenApiParameter(name='mois', description='Mois (1-12)', required=False, type=int),
            OpenApiParameter(name='annee', description='Année (ex: 2026)', required=False, type=int),
        ],
        responses={200: TransactionListSerializer(many=True)}
    )
    def get(self, request):
        filters = {
            'compte_id': request.query_params.get('compte_id'),
            'categorie_id': request.query_params.get('categorie_id'),
            'type': request.query_params.get('type'),
            'mois': request.query_params.get('mois'),
            'annee': request.query_params.get('annee'),
        }
        filters = {k: v for k, v in filters.items() if v is not None}

        transactions = TransactionService.get_transactions_user(
            request.user,
            filters=filters
        )
        serializer = TransactionListSerializer(
            transactions,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=TransactionDetailSerializer, responses=TransactionDetailSerializer)
    def post(self, request):
        serializer = TransactionDetailSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionDetailSerializer # Correction Swagger

    def get_object(self, request, pk):
        return TransactionService.get_transaction_by_id(request.user, pk)

    def get(self, request, pk):
        transaction = self.get_object(request, pk)
        if not transaction:
            return Response(
                {'error': 'Transaction introuvable.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = TransactionDetailSerializer(
            transaction,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        transaction = self.get_object(request, pk)
        if not transaction:
            return Response(
                {'error': 'Transaction introuvable.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = TransactionDetailSerializer(
            transaction,
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        transaction = self.get_object(request, pk)
        if not transaction:
            return Response(
                {'error': 'Transaction introuvable.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = TransactionDetailSerializer(
            transaction,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        transaction = self.get_object(request, pk)
        if not transaction:
            return Response(
                {'error': 'Transaction introuvable.'},
                status=status.HTTP_404_NOT_FOUND
            )
        TransactionService.supprimer_transaction(transaction)
        return Response(
            {'message': 'Transaction supprimée avec succès.'},
            status=status.HTTP_204_NO_CONTENT
        )


class TransactionStatistiquesView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='mois', description='Mois', required=True, type=int),
            OpenApiParameter(name='annee', description='Année', required=True, type=int),
        ],
        responses={200: dict}
    )
    def get(self, request):
        mois = request.query_params.get('mois')
        annee = request.query_params.get('annee')

        if not mois or not annee:
            return Response(
                {'error': 'Les paramètres mois et annee sont requis.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            mois = int(mois)
            annee = int(annee)
        except ValueError:
            return Response(
                {'error': 'Les paramètres mois et annee doivent être des entiers.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        bilan = TransactionService.get_bilan_mensuel(
            request.user, mois, annee
        )
        depenses_par_categorie = FinanceCalculator.calculer_depenses_par_categorie(
            request.user, mois, annee
        )

        return Response({
            'bilan': bilan,
            'depenses_par_categorie': depenses_par_categorie,
        }, status=status.HTTP_200_OK)
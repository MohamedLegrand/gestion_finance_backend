from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter # Import important
from finances.api.serializers.budget_serializer import BudgetSerializer
from finances.services.budget_service import BudgetService


class BudgetListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetSerializer # <--- Correction pour Swagger

    @extend_schema(
        parameters=[
            OpenApiParameter(name='mois', description='Mois du budget', required=False, type=int),
            OpenApiParameter(name='annee', description='Année du budget', required=False, type=int),
        ]
    )
    def get(self, request):
        mois = request.query_params.get('mois')
        annee = request.query_params.get('annee')

        budgets = BudgetService.get_budgets_user(
            request.user,
            mois=mois,
            annee=annee
        )
        serializer = BudgetSerializer(
            budgets,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BudgetSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BudgetDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetSerializer # <--- Correction pour Swagger

    def get_object(self, request, pk):
        return BudgetService.get_budget_by_id(request.user, pk)

    def get(self, request, pk):
        budget = self.get_object(request, pk)
        if not budget:
            return Response(
                {'error': 'Budget introuvable.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = BudgetSerializer(
            budget,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        budget = self.get_object(request, pk)
        if not budget:
            return Response(
                {'error': 'Budget introuvable.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = BudgetSerializer(
            budget,
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        budget = self.get_object(request, pk)
        if not budget:
            return Response(
                {'error': 'Budget introuvable.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = BudgetSerializer(
            budget,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        budget = self.get_object(request, pk)
        if not budget:
            return Response(
                {'error': 'Budget introuvable.'},
                status=status.HTTP_404_NOT_FOUND
            )
        BudgetService.supprimer_budget(budget)
        return Response(
            {'message': 'Budget supprimé avec succès.'},
            status=status.HTTP_204_NO_CONTENT
        )


class BudgetEtatView(APIView):
    permission_classes = [IsAuthenticated]
    # Pas de serializer_class ici car on retourne un dictionnaire personnalisé

    @extend_schema(
        parameters=[
            OpenApiParameter(name='mois', description='Mois', required=True, type=int),
            OpenApiParameter(name='annee', description='Année', required=True, type=int),
        ],
        responses={200: dict} # Indique à Swagger que la réponse est un objet JSON
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

        etat = BudgetService.get_etat_tous_budgets(
            request.user, mois, annee
        )
        return Response(etat, status=status.HTTP_200_OK)
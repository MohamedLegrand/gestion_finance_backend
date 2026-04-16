from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from dashboard.services.dashboard_service import DashboardService
from dashboard.api.serializers.dashboard_serializer import DashboardSerializer


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DashboardSerializer

    @extend_schema(
        operation_id='dashboard_retrieve',
        summary="Dashboard principal",
        description="""
            Retourne toutes les données du dashboard pour l'utilisateur connecté :
            - Solde total de tous les comptes
            - Bilan du mois en cours (revenus, dépenses, épargne)
            - 5 dernières transactions
            - Dépenses par catégorie du mois
            - État de tous les budgets du mois
        """,
        responses={200: DashboardSerializer},
    )
    def get(self, request):
        try:
            data = DashboardService.get_dashboard_data(request.user)
            serializer = DashboardSerializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
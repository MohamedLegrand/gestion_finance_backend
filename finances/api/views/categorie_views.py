from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter # Ajout pour la doc
from finances.models.categorie_model import Categorie
from finances.api.serializers.categorie_serializer import CategorieSerializer


class CategorieListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorieSerializer # <--- Correction Swagger (Guess serializer)

    @extend_schema(
        parameters=[
            OpenApiParameter(name='type', description='Filtrer par type (depense ou revenu)', required=False, type=str),
        ]
    )
    def get(self, request):
        # On récupère le type depuis les query params
        type_cat = request.query_params.get('type')
        categories = Categorie.objects.filter(user=request.user)
        
        if type_cat:
            categories = categories.filter(type=type_cat)
            
        serializer = CategorieSerializer(
            categories,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorieSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategorieDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorieSerializer # <--- Correction Swagger

    def get_object(self, request, pk):
        try:
            return Categorie.objects.get(id=pk, user=request.user)
        except Categorie.DoesNotExist:
            return None

    def get(self, request, pk):
        categorie = self.get_object(request, pk)
        if not categorie:
            return Response(
                {'error': 'Catégorie introuvable.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategorieSerializer(
            categorie,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        categorie = self.get_object(request, pk)
        if not categorie:
            return Response(
                {'error': 'Catégorie introuvable.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategorieSerializer(
            categorie,
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        categorie = self.get_object(request, pk)
        if not categorie:
            return Response(
                {'error': 'Catégorie introuvable.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategorieSerializer(
            categorie,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        categorie = self.get_object(request, pk)
        if not categorie:
            return Response(
                {'error': 'Catégorie introuvable.'},
                status=status.HTTP_404_NOT_FOUND
            )
        categorie.delete()
        return Response(
            {'message': 'Catégorie supprimée avec succès.'},
            status=status.HTTP_204_NO_CONTENT
        )
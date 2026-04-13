"""
URL configuration for gestion_finance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

# Importation des vues nécessaires pour la documentation Swagger (OpenAPI)
from drf_spectacular.views import (
    SpectacularAPIView,          # Génère le schéma OpenAPI (fichier JSON/YAML)
    SpectacularSwaggerView,      # Interface interactive Swagger UI
    SpectacularRedocView,        # Interface alternative ReDoc
)

urlpatterns = [
    # Administration Django
    path('admin/', admin.site.urls),

    # Vos endpoints API existants (gestion des comptes)
    path('api/account/', include('account.api.urls')),

    # module finances
    path('api/finances/', include('finances.api.urls')),

    # ==============================================
    # Documentation automatique de l'API (Swagger)
    # ==============================================

    # Endpoint qui expose le schéma OpenAPI brut (format JSON)
    # Utile pour des outils tiers ou une génération de client API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Interface utilisateur Swagger UI (recommandée, très visuelle et interactive)
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Interface alternative ReDoc (présentation plus structurée en colonnes)
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

     # Token refresh
    path('api/account/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
from django.urls import path
from .views.auth_views import RegisterView, LoginView
from .views.profile_views import ProfileView
from .views.refreshtoken_view import RefreshTokenView


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
]
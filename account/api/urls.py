from django.urls import path
from .views.auth_views import RegisterView, LoginView
from .views.profile_views import ProfileView


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', ProfileView.as_view()),
]
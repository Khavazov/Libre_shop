from django.urls import path

from .views import RegistrationAPIView, ActivationView, LoginView, LogoutView

urlpatterns = [
    path('register/', RegistrationAPIView.as_view()),
    path('activate/<str:activation_code>/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]
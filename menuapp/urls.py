from django.urls import path
from .views import RegisterView, EmailConfirmView, LoginView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm-email/<uuid:token>/', EmailConfirmView.as_view(), name='confirm_email'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]


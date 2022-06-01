from django.urls import path
from .views import LoginView, RegistrationView, VerifyEmailView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login_view'),
    path('register-user/', RegistrationView.as_view(), name='Registration_View'),
    path('verify-user/', VerifyEmailView.as_view(), name='Registration_View'),
]
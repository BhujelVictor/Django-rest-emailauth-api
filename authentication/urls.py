from django.urls import path
from authentication.views import *
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register-user'),
    path('login/', UserLoginView.as_view(), name='login-user'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='change-password'),
    path('password-reset-email/', SendPasswordResetEmailView.as_view(), name='password-reset-email'),
    path('password-reset/<uid>/<token>/', UserPasswordResetView.as_view(), name='password-reset'),
]

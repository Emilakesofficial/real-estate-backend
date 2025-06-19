from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('verify-email/', VerifyEmailView.as_view()),
    path('resend-token/', ResendEmailView.as_view()),
    path('login/', LoginView.as_view()),
    path('get-profile/', ProfileView.as_view()),
    path('update-profile/', ProfileView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('countries/', CountryView.as_view()),
    path('update-country/<int:pk>/', CountryUpdateView.as_view()),
    path('verify-old-password/', VerifyOldPasswordView.as_view()),
    path('verify-password-otp/', VerifyOTPView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('verify-forget-password-otp/', VerifyPasswordOTPView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('add-passcode/', PasscodeView.as_view()),
]
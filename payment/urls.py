from django.urls import path
from .views import *

urlpatterns = [
    path('initialize/', InitializePaymentView.as_view()),
    path('verify/', VerifyPaymentView.as_view()),
    # path('webhook/', paystack_webhook),
]

from django.urls import path
from .views import CartView, AddToCartView, RemoveFromCartView

urlpatterns = [
    path('cart/', CartView.as_view(),),
    path('cart/add/<int:property_id>/', AddToCartView.as_view()),
    path('cart/remove/<int:property_id>/', RemoveFromCartView.as_view()),
]

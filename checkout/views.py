from django.conf import settings
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from listings.models import Property
from .serializers import CartSerializer
from django.views.decorators.csrf import csrf_exempt


class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, property_id):
        user = request.user
        property_obj = get_object_or_404(Property, id=property_id, is_active=True, is_published=True)
        cart, created = Cart.objects.get_or_create(user=user)

        if CartItem.objects.filter(cart=cart, property=property_obj).exists():
            return Response({'detail': 'Property already in cart.'}, status=status.HTTP_400_BAD_REQUEST)

        CartItem.objects.create(cart=cart, property=property_obj)
        return Response({'message': 'Property added to cart.'}, status=status.HTTP_201_CREATED)

class RemoveFromCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, property_id):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        property_obj = get_object_or_404(Property, id=property_id)

        try:
            item = CartItem.objects.get(cart=cart, property=property_obj)
            item.delete()
        except CartItem.DoesNotExist:
            return Response({'detail': 'Property not found in cart.'}, status=status.HTTP_404_NOT_FOUND)

        # Delete cart if empty
        if not cart.items.exists():
            cart.delete()
            return Response({'message': 'Property removed. Cart is now empty and deleted.'}, status=status.HTTP_200_OK)

        return Response({'message': 'Property removed from cart.'}, status=status.HTTP_200_OK)



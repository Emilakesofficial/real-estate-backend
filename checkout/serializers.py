from rest_framework import serializers
from .models import *
from listings.models import Property

class PropertyMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'title', 'price']

class CartItemSerializer(serializers.ModelSerializer):
    property = PropertyMiniSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'property', 'added_at']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'created_at']
        read_only_fields = ['user']

    def get_total_price(self, obj):
        return obj.total_price()


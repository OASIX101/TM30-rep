from rest_framework import serializers
from .models import Cart, Item

class ItemSerializer(serializers.ModelSerializer):
    orders = serializers.ReadOnlyField()

    class Meta:
        model = Item
        fields = ['item_name', 'price', 'quantity_available', 'item_description', 'orders']

class CartSerializer(serializers.ModelSerializer):
    cart_content = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ['id', 'user' ,'cart_item', 'quantity', 'item_cost', 'date_ordered', 'status', 'cart_content', 'date_ordered']
        
class CartReqSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['cart_item', 'quantity']

class ItemUserSerializer(serializers.ModelSerializer):
    orders_count = serializers.ReadOnlyField()

    class Meta:
        model = Item
        fields = ['item_name', 'price', 'quantity_available', 'item_description', 'orders_count']

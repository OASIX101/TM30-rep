from django.contrib import admin
from .models import Cart, Item

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_item', 'status')
    list_filter = ('status', 'user', 'cart_item')
    search_fields = ('status', 'user', 'cart_item')
    raw_id_fields = ('user',)
    list_editable = ['status']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display_links = ('item_name',)
    list_display = ('item_name', 'price', 'quantity_available')
    list_filter = ('item_name', 'quantity_available')
    search_fields = ('item_name', 'quantity_available')
    list_editable = ['quantity_available', 'price']
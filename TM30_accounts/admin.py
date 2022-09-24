from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CartAdmin(admin.ModelAdmin):
    list_display_links = ('username',)
    list_display = ('username', 'first_name', 'last_name', 'email', 'gender')
    list_filter = ('username', 'gender', 'is_staff')
    search_fields = ('username', 'gender', 'is_staff')
    list_editable = ['email', 'gender']
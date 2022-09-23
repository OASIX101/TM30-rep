from django.contrib import admin
from .models import Cart, Item

admin.site.register([Cart, Item])

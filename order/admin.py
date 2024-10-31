from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class UserCartAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__email',)


@admin.register(CartItem)
class UserCartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product')

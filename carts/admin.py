from django.contrib import admin
from .models import Cart, CartItem
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    #the list the show up after clicking the email address of the user
    list_display = ('cart_id', 'date_added')
    readonly_fields = ('cart_id',)

class CartItemAdmin(admin.ModelAdmin):
    #the list the show up after clicking the email address of the user
    list_display = ('product', 'user', 'cart', 'quantity', 'is_active', 'cart_id')

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)

# sales/admin.py

from django.contrib import admin
from .models import Product, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ['name', 'price', 'stock', 'is_active']  # ✅ removed category
    list_filter   = ['is_active']                             # ✅ removed category
    search_fields = ['name']                                  # ✅ removed barcode
    ordering      = ['name']


class OrderItemInline(admin.TabularInline):
    model  = OrderItem
    extra  = 1
    fields = ['product', 'quantity', 'price']                 # ✅ unit_price → price


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ['pk', 'cashier', 'status', 'created_at']
    list_filter   = ['status']
    search_fields = ['cashier__username', 'notes']            # ✅ fixed cashier lookup
    ordering      = ['-created_at']
    inlines       = [OrderItemInline]
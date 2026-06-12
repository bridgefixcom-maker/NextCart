from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'price', 'quantity', 'subtotal')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'status', 'total_amount', 'is_paid', 'payment_method', 'created_at')
    list_filter   = ('status', 'is_paid', 'payment_method')
    search_fields = ('user__email', 'full_name', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    inlines       = [OrderItemInline]

    list_editable = ['status']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display  = ('order', 'product_name', 'price', 'quantity', 'subtotal')
    search_fields = ('product_name', 'order__user__email')

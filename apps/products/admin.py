from django.contrib import admin
from .models import Category, Product, ProductImage


# admin.site.register(Category)
# admin.site.register(Product)
# admin.site.register(ProductImage)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'is_primary']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'sku', 'price', 'sale_price', 'stock_quantity', 'is_available', 'in_stock']
    list_filter = ['is_available', 'category']
    search_fields = ['name', 'sku', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['sku', 'slug', 'created_at', 'updated_at', 'discount_percentage', 'effective_price']
    inlines = [ProductImageInline]
    ordering = ['name']

    fieldsets = (
        ('Basic Info', {
            'fields': ('category', 'name', 'slug', 'sku', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'sale_price', 'effective_price', 'discount_percentage')
        }),
        ('Stock', {
            'fields': ('stock_quantity', 'is_available')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def in_stock(self, obj):
        return obj.in_stock
    in_stock.boolean = True
    in_stock.short_description = 'In Stock'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'is_primary', 'created_at']
    list_filter = ['is_primary']

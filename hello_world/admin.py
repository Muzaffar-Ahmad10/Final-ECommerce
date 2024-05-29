from django.contrib import admin
from .models import Product, ProductImage, CartItem, SoldProduct, ContactUs


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at', 'updated_at')
    inlines = [ProductImageInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(CartItem)
admin.site.register(SoldProduct)
admin.site.register(ContactUs)
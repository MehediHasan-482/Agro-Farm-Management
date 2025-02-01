from django.contrib import admin
from .models import Product,ProductImage,Category,Coupon


class ProductImageAdmin(admin.StackedInline):
    model=ProductImage

class ProductAdmin(admin.ModelAdmin):
    inlines=[ProductImageAdmin]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(Coupon)



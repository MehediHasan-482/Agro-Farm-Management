from django.contrib import admin
from .models import Animal,Order,Profile,Cart,CartItems

# Register your models here.

admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(Animal)
admin.site.register(Order)

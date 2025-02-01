from django.urls import path
from products.views import get_product

urlpatterns = [

    path('<slug:slug>/', get_product, name='get_product'),

]
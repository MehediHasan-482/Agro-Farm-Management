from django.urls import path
from home.views import index,portfolio_view

urlpatterns = [

    path('', index, name="index"), 
    path('portfolio/', portfolio_view, name='portfolio'),

]
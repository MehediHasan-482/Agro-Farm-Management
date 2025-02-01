from django.urls import path, reverse
from . import views
import search
app_name = 'search'

urlpatterns = [
	path('', views.search, name = "search"),
]

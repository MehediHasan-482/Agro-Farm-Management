from django.urls import path
from accounts.views import buy_now, download_pdf, forgot_password, login_page, logout_page, my_order, process_payment,remove_cart, user_profile
from accounts.views import register_page,activate_email,add_to_cart,cart
# from .models import views
# from products.views import

urlpatterns = [
     path('login/',login_page, name="login"),
     path('register/', register_page, name="register"),
     path('logout/',logout_page,name="logout"),
     path('user_profile/', user_profile, name='user_profile'),
     path('activate/<email_token>/', activate_email, name="activate_email"),
     path('cart/',cart,name="cart"),
     path('add-to-cart/<u_id>/',add_to_cart,name="add_to_cart"),
     path('remove-cart/<cart_item_uid>/', remove_cart, name="remove_cart"),
     path('process_payment/', process_payment, name='process_payment'),
     path('download_pdf/', download_pdf, name='download_pdf'),
     path('buy_now/<u_id>/',buy_now, name='buy_now'),
     path('my_order/', my_order, name='my_order'),
     path('forgot-password/', forgot_password, name='forgot_password'),
     

]
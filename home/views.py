from django.shortcuts import render
from home.models import Portfolio
from products.models import Coupon, Product


# Create your views here.

def index(request):
    coupons = Coupon.objects.all()
    context = {'products' : Product.objects.all(),'coupons':coupons}
    return render(request,'home/index.html', context)

def portfolio_view(request):
    portfolio_items = Portfolio.objects.all()
    return render(request, 'home/portfolio.html', {'portfolio': portfolio_items})



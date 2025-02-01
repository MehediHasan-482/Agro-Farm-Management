from django.shortcuts import redirect, render
from products.models import Category, Coupon, Product
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

def get_product(request, slug):

    # print('******')
    # print(request.user)
    # print('******')
    # print(request.user.profile.get_cart_count)
    try:
        print("Trying to fetch product")
        product = Product.objects.get(slug=slug)
        print("Product found:", product)
        context = {'product': product}
        return render(request, 'products/product.html', context=context)

    except Exception as e:
        print("Error occurred:", e)
        return HttpResponse("An error occurred.", status=500)



# def add_to_cart(request,slug):

#     category=request.GET.get('category')
#     product=Product.objects.get(slug=slug)
#     user=request.user
#     cart,_=Cart.objects.get_or_create(user=user,is_paid=False)

#     cart_items= CartItems.objects.create(cart=cart,product=product)

#     if category:
#         category=request.GET.get('category')
#         category_name=Category.objects.get(category_name=category)
#         cart_items.category_name=category_name
#         cart_items.save()

#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
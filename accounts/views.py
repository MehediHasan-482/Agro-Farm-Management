from io import BytesIO
import string
from tkinter import Canvas
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from accounts.models import send_email_token
from base.email import send_account_activation_email 
from django.views.decorators.csrf import csrf_exempt
from .models import Order, Profile
from products.models import *
from array import *
from accounts.models import Cart,CartItems
from django.http import HttpResponseRedirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
import random


# Create your views here.

@csrf_exempt
def login_page(request):
        
    if request.method == 'POST':   
        email=request.POST.get('email')
        password=request.POST.get('password')
        user_obj = User.objects.filter(username=email)
        print('hello1')

        if not user_obj.exists():
            messages.warning(request, "Account not found.")
            print('hello2')
            return HttpResponseRedirect(request.path_info)    

        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, "your account is not verified.")
            print('hello3')
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username=email,password=password )
        print(user_obj)
        print('hello6')
        if user_obj:
            # print('email',email)
            # print('password',password)
            # messages.success(request, "Your account has been created successfully.")
            login(request, user_obj)
            messages.success(request, "An email has been sent on your mail.")
            # return render(request,'home/index.html')
            return redirect('/')

        messages.warning(request, "Invalid credential.")
        return HttpResponseRedirect(request.path_info)


    return render(request, 'accounts/login.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if not user:
            messages.warning(request, "No account found with this email address.")
            return HttpResponseRedirect(request.path_info)

        # Generate a random password
        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        # Set the new password
        user.set_password(new_password)
        user.save()

        # Send the email
        send_mail(
            subject="Password Reset - Your New Password",
            message=f"Your new password is: {new_password}\nPlease log in and change your password immediately.",
            from_email="noreply@example.com",
            recipient_list=[email],
            fail_silently=False,
        )

        messages.success(request, "A new password has been sent to your email.")
        return redirect('login')  # Redirect to the login page after sending the email

    return render(request, 'accounts/forgot_password.html')



@csrf_exempt
def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Email format validation
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email format. Please enter a valid email.")
            return HttpResponseRedirect(request.path_info)
        
        # Check if the email is already taken
        user_obj = User.objects.filter(username=email)
        if user_obj.exists():
            messages.warning(request, "Email is already taken.")
            return HttpResponseRedirect(request.path_info)

        # Create the user if validation passes
        user_obj = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=email
        )
        user_obj.set_password(password)
        user_obj.save()

        # Send a success message
        messages.success(request, "An email has been sent to your mail.")
        # Uncomment the next line if you have email sending logic
        # send_account_activation_email(email)
        return HttpResponseRedirect(request.path_info)
    
    return render(request, 'accounts/register.html')


def logout_page(request):
    logout(request)
    return redirect('/')

# def reverse_hashing_example(): 
#     # Replace this logic with securely storing plain passwords if required.
#     return "original_password"

@login_required 
def user_profile(request):
    user = request.user
    
    if request.method == "POST":
        # Update profile information
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)

        # Update password securely
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if current_password and new_password and confirm_password:
            if user.check_password(current_password):
                if new_password == confirm_password:
                    user.set_password(new_password)  # Hash the new password
                    user.save()
                    update_session_auth_hash(request, user)  # Keep the user logged in
                    messages.success(request, "Password updated successfully.")
                else:
                    messages.error(request, "New password and confirmation do not match.")
            else:
                messages.error(request, "Current password is incorrect.")
        else:
            messages.error(request, "Please fill in all password fields to update the password.")
        
        user.save()
        return redirect('user_profile')
    
    return render(request, 'accounts/profile.html', {'user': user})



def activate_email(request,email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_verified=True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse('Invalied Email Token')


@login_required
def add_to_cart(request,u_id):

    category=request.GET.get('category')
    product=Product.objects.get(u_id=u_id)
    print(product.product_code)
    # product1=product.product_code
    # request.session['product1'] = product1
    user=request.user
    cart,_=Cart.objects.get_or_create(user=user,is_paid=False)            

    cart_items= CartItems.objects.create(cart=cart,product=product,user=request.user)

    if category:
        category=request.GET.get('category')
        category_name=Category.objects.get(category_name=category)
        cart_items.category_name=category_name
        cart_items.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_cart(request,cart_item_uid):
    try:
        cart_item=CartItems.objects.get(u_id=cart_item_uid)
        cart_item.delete()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
def cart(request):   
    cart = Cart.objects.filter(is_paid=False, user=request.user).first()
    cart_items = CartItems.objects.filter(cart=cart)
    sum_of_price = 0
    discount = 0  # Initialize discount value

    # Calculate the total price of items in the cart
    for item in cart_items:
        item.total_price = item.product.per_kg_cost * item.product.weight
        sum_of_price += item.total_price

    # Store the original sum_of_price in the session
    request.session['sum_of_price'] = sum_of_price

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code=coupon_code).first()

        if not coupon_obj:
            messages.warning(request, "Invalid Coupon.")
        elif coupon_obj.is_expired:
            messages.warning(request, "This coupon is expired.")
        elif sum_of_price < coupon_obj.minimum_amount:
            messages.warning(
                request,
                f"Minimum purchase amount for this coupon is {coupon_obj.minimum_amount}."
            )
        else:
            # Apply discount if the coupon is valid
            discount = coupon_obj.discount_price
            sum_of_price -= discount  # Update sum_of_price with the discounted value
            request.session['discounted_sum_of_price'] = sum_of_price  # Store discounted price
            messages.success(request, "Coupon applied successfully!")

    # Pass sum_of_price and discount to the template
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'sum_of_price': sum_of_price,  # This will either be the original or discounted price
        'discount': discount,
    }
    return render(request, 'accounts/cart.html', context)


@csrf_exempt
def process_payment(request):
    email = request.user.email

    # Check if a discounted price is available, otherwise use the original sum_of_price
    discounted_sum_of_price = request.session.get('discounted_sum_of_price')
    original_sum_of_price = request.session.get('sum_of_price')

    # Determine the amount to be used for payment
    amount = discounted_sum_of_price if discounted_sum_of_price else original_sum_of_price

    if not amount:
        messages.error(request, "No cart total found. Please try again.")
        return redirect('cart')

    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')
        trnxID = request.POST.get('trnx')

        # Ensure all required fields are filled
        if not all([name, email, address, amount, payment_method]):
            messages.error(request, "Please fill out all fields.")
            return redirect('process_payment')

        # Save payment data to the session
        request.session['payment_data'] = {
            'name': name,
            'email': email,
            'address': address,
            'amount': amount,
            'payment_method': payment_method,
            'trnxID': trnxID,
        }

        # Get cart and cart items
        cart = Cart.objects.filter(is_paid=False, user=request.user).first()
        cart_items = CartItems.objects.filter(cart=cart)
        product_code = [item.product.product_code for item in cart_items]

        # Create an order
        order_items = Order.objects.create(
            customer_name=name,
            product_code=product_code,
            customer_email=email,
            customer_address=address,
            amount=amount,
            payment_method=payment_method,
            transaction_id=trnxID
        )
        order_items.save()

        # Mark the cart as paid
        cart.is_paid = True
        cart.save()

        messages.success(request, "Payment successful.")
        return redirect('process_payment')

    return render(request, 'accounts/buy.html', {'amount': amount})




def buy_now(request, u_id):
    try:
        product = Product.objects.get(u_id=u_id)
        amount = product.per_kg_cost * product.weight

        if request.method == 'POST':
            return _extracted_from_buy_now_8(request, amount, product.product_code)

        context = {
            'product': product,
            'amount': amount
        }
        return render(request, 'accounts/buy.html', context=context)

    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect('home')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('home')



# TODO Rename this here and in buy_now
def _extracted_from_buy_now_8(request, amount, prod):
    # Collect submitted data
    name = request.POST.get('name')
    email = request.POST.get('email')
    address = request.POST.get('address')
    # amount = request.POST.get('amount')
    payment_method = request.POST.get('payment_method')
    trnxID=request.POST.get('trnx')

    # Check if all fields are filled
    if not all([name, email, address, amount, payment_method]):
        messages.error(request, "Please fill out all fields.")
        return redirect('process_payment')

    request.session['payment_data'] = {
        'name': name,
        'email': email,
        'address': address,
        'amount': amount,
        'payment_method': payment_method,
        'trnxID':trnxID,
    }

    # product=Product.objects.get(u_id=u_id)
    # user=request.user
    # Display success message and redirect
    # product=Product.objects.all(u_id=u_id)
    # prod=product.product_code
    # print(prod)
    order_items= Order.objects.create(customer_name=name,product_code=prod,customer_email=email,customer_address=address,amount=amount,payment_method=payment_method,transaction_id=trnxID)
    order_items.save()
    messages.success(request, "Payment successful.")
    return redirect('buy_now') # Redirect to avoid duplicate submissions



# Generate and download a PDF with user information
def download_pdf(request):
    try:
        user_data = request.session.get('payment_data')

        if not user_data:
            messages.error(request, "No data available for PDF generation.")
            return redirect('cart')

        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)

        pdf.drawString(100, 750, "Payment Slip")
        pdf.drawString(100, 730, f"Name: {user_data['name']}")
        pdf.drawString(100, 710, f"Email: {user_data['email']}")
        pdf.drawString(100, 690, f"Address: {user_data['address']}")
        pdf.drawString(100, 670, f"Amount: {user_data['amount']}")
        pdf.drawString(100, 650, f"Payment Method: {user_data['payment_method']}")
        pdf.drawString(100, 630, f"Transaction_id: {user_data['trnxID']}")

        pdf.save()

        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="payment_slip.pdf"'
        return response

    except Exception as e:
        return HttpResponse(f"An error occurred while generating the PDF: {str(e)}")


def my_order(request):
    orders = Order.objects.filter(customer_email=request.user.email)
    print(orders)
    return render(request, 'accounts/my_order.html', {'orders': orders})
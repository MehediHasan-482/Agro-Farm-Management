from pickle import APPEND, APPENDS
from urllib import request
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.shortcuts import render
from base.email import send_account_activation_email
from base.models import BaseModel
from django.db.models.signals import post_save
import uuid
from products.models import Product,Category
import random
from products.models import Product


class Profile(BaseModel):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    is_email_verified=models.BooleanField(default=False)
    email_token=models.CharField(max_length=100,null=True,blank=True)
    profile_image=models.ImageField(upload_to='profile')

    def get_cart_count(self):
        return CartItems.objects.filter(cart__is_paid=False, cart__user=self.user).count()
    

@receiver(post_save, sender=User)
def send_email_token(sender,instance,created,**kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())           
            Profile.objects.create(user = instance , email_token = email_token)
            email = instance.email
            send_account_activation_email(email,email_token)

    except Exception as e:
        print(e)




class Cart(BaseModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name='carts')
    is_paid=models.BooleanField(default=False)


    def __str__(self):
        return f'{self.user}'



class CartItems(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart= models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    category=models.ForeignKey(Category, on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return f'{self.product} - by {self.user}'


class Animal(models.Model):
    a_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    animal_tag = models.CharField(max_length=4, unique=True, editable=False)
    category=models.ForeignKey(Category, on_delete=models.SET_NULL,null=True,blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender =models.CharField(max_length=20)
    discription=models.TextField()
    animal_image=models.ImageField(upload_to='animal_profile')


    def save(self, *args, **kwargs):
        if not self.animal_tag:
            self.animal_tag = self.generate_animal_tag()
        super().save(*args, **kwargs)

    def generate_animal_tag(self):
        while True:
            tag = f"{random.randint(1000, 9999)}"
            if not Animal.objects.filter(animal_tag=tag).exists():
                return tag
            
    def __str__(self):
        return f'{self.category} ->   Animal tag-{self.animal_tag}'
    


class Order(BaseModel):
    customer_name = models.CharField(max_length=20)
    product_code = models.TextField()
    customer_email = models.EmailField()
    customer_address = models.TextField()
    amount = models.IntegerField()
    payment_method = models.CharField(max_length=20)
    transaction_id = models.TextField()

    def __str__(self):
        return f"{self.customer_email} - {self.product_code}"
    

      


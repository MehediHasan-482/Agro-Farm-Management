import random
from django.db import models
from accounts import apps
from base.models import BaseModel
from django.utils.text import slugify


class Category(BaseModel):
    # category=models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category_image = models.ImageField(upload_to="categories")

    def save(self, *args, **kwargs):
        self.slug=slugify(self.category_name)
        super(Category,self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name


class Product(BaseModel):
    # product=models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    product_code=models.TextField()
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    age = models.CharField(max_length=50)
    weight = models.IntegerField()
    colour = models.CharField(max_length=100)
    per_kg_cost = models.IntegerField()
    product_description = models.TextField()
    ription = models.TextField() 


    def save(self, *args, **kwargs):
        self.slug=slugify(self.product_name)
        super(Product,self).save(*args, **kwargs)

    def __str__(self)->str:
        return self.product_name

class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to="product")
    

class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=200000)

 

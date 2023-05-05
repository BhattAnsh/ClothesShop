from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100, default="")
    product_details = models.CharField(max_length=500, default="")
    product_cat = models.CharField(max_length=50, default="")
    product_sub_cat = models.CharField(max_length=50, default="")
    product_price = models.DecimalField(max_digits=100000, decimal_places=3, default=0.0)
    product_main_image = models.ImageField(upload_to='shop/images', default="")
    prod_image_1 = models.ImageField(upload_to='shop/images', default="")
    prod_image_2 = models.ImageField(upload_to='shop/images', default="")
    prod_image_3 = models.ImageField(upload_to='shop/images', default="")
    prod_image_4 = models.ImageField(upload_to='shop/images', default="")

    def __str__(self):
        return self.product_name

class Sale(models.Model):
    sale_id = models.AutoField(primary_key=True)
    sale_name = models.CharField(max_length=50, default="")
    sale_image = models.ImageField(upload_to='shop/images', default="")

    def __str__(self):
        return self.sale_name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Uaddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="")
    email = models.EmailField(default="")
    add1 = models.CharField(max_length=1000, default="")
    add2 = models.CharField(max_length=1000, default="")
    country = models.CharField(max_length=100, default= "")
    state = models.CharField(max_length=100, default="")
    zip = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

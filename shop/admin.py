from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Uaddress)
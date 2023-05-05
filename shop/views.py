from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import *
import json
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout


#getting the values
distinct_categories = Product.objects.values('product_cat').distinct()
cats = []
for i in distinct_categories:
    cats.append(list(i.values())[0])
# Create your views here.

def gettingCartItem(user):
    cart_products = CartProduct.objects.filter(cart__user__username=user)
    total_cart = 0
    for i in cart_products:
        total_cart += i.quantity
    return total_cart

def index(request):
    #getting the data from the database
    p = Product.objects.all()
    s = Sale.objects.all()
    if gettingCartItem(request.user) == 0:
        total = ""
    else:
        total = gettingCartItem(request.user)
    no_of_cats = len(distinct_categories)
    params = {'Prods':p, 'sale':s, 'cats': no_of_cats,'cats_list': cats, 'user': request.user,'totalItem':total}
    return render(request, 'index.html', params)

def productPage(request, myid):
    prod = Product.objects.filter(product_id = myid)
    if gettingCartItem(request.user) == 0:
        total = ""
    else:
        total = gettingCartItem(request.user)
    context = {'prod': prod, 'totalItem':total}
    return render(request, 'product.html', context)

def productList(request):
    if gettingCartItem(request.user) == 0:
        total = ""
    else:
        total = gettingCartItem(request.user)
    context = {'totalItem':total, 'user':request.user}
    return render(request, 'product-list.html', context)

def addToCart(request):
    if request.method == 'POST':
        prod_id = request.POST.get('productId')
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        prod = Product.objects.get(product_id=prod_id)
        cart_product, created = CartProduct.objects.get_or_create(cart = cart, product = prod)
        if not created:
            cart_product.quantity += 1
            cart_product.save()
        else:
            cart.products.add(cart_product)
    if gettingCartItem(request.user) == 0:
        total = ""
    else:
        total = gettingCartItem(request.user)
    context = {'totalItem':total}
    return JsonResponse(context)

def removeFromCart(request):
    #getting the post request from the user
    if request.method == 'POST':
        prod_id = request.POST.get('productId')
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        prod = Product.objects.get(product_id=prod_id)
        cart_product, created = CartProduct.objects.get_or_create(cart = cart, product = prod)
    #removing the product from the cart 
        if not created:
            cart_product.quantity -= 1
            cart_product.save()
        qty = cart_product.quantity
        cart_products = CartProduct.objects.filter(cart__user__username=request.user)
        lst = []
        for i in cart_products:
            lst.append(i.product.product_price * i.quantity)
        formatted = "{:,.2f}".format(sum(lst))
    #if the product quantity in the cart become 0 deleting the product from the cart
    if cart_product.quantity == 0:
        lst = CartProduct.objects.get(cart__user__username=request.user,product__product_name=cart_product.product.product_name)
        lst.delete()
    if gettingCartItem(request.user) == 0:
        total = ""
    else:
        total = gettingCartItem(request.user)
    context = {'totalItem':total,'qty':qty, 'total':formatted}
    return JsonResponse(context)

def showCart(request):
    cart_products = CartProduct.objects.filter(cart__user__username=request.user)
    if len(cart_products) == 0:
        return render(request, 'emptyCart.html')
    else:
        lst = []
        for i in cart_products:
            lst.append(i.product.product_price * i.quantity)
    if gettingCartItem(request.user) == 0:
        total = ""
    else:
        total = gettingCartItem(request.user)
        formatted = "{:,.2f}".format(sum(lst))   
        context = {'prods':cart_products, 'sum':formatted,'totalItem':total}
        return render(request,'cart.html', context)
         
def checkout(request):
    cart_products = CartProduct.objects.filter(cart__user__username=request.user)
    lst = []
    for i in cart_products:
        lst.append(i.product.product_price * i.quantity)
    if gettingCartItem(request.user) == 0:
        total = ""
    else:
        total = gettingCartItem(request.user)
    formatted = "{:,.2f}".format(sum(lst))   
    context = {'prods':cart_products, 'totalItem':total, 'items':len(cart_products), 'sum': formatted}
    return render(request, 'checkout.html', context)

def confirmOrder(request):
    if request.method == 'POST':
        user = request.user
        name = request.POST.get('name')
        email = request.POST.get('email')
        add1 = request.POST.get('add1')
        add2 = request.POST.get('add2')
        country = request.POST.get('country')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        check = request.POST.get('save-info') == 'on'

        try:
            # Try to get an existing address
            address = Uaddress.objects.get(user=user)
            # Update the address fields
            address.name = name
            address.email = email
            address.add1 = add1
            address.add2 = add2
            address.country = country
            address.state = state
            address.zip = zip
            address.save()
        except Uaddress.DoesNotExist:
            # An address for the user doesn't exist, create a new one with the specified fields
            address = Uaddress.objects.create(
                user=user,
                name=name,
                email=email,
                add1=add1,
                add2=add2,
                country=country,
                state=state,
                zip=zip,
            )
        if check:
            address.save()
    Cart.objects.filter(user = user).delete()
    cart_products = CartProduct.objects.filter(cart__user__username=request.user)
    lst = []
    for i in cart_products:
        lst.append(i.product.product_price * i.quantity)
    if gettingCartItem(request.user) == 0:
        total = ""
    else:
        total = gettingCartItem(request.user)
    formatted = "{:,.2f}".format(sum(lst)) 
    context = {'prods': cart_products, 'totalItem':total, 'sum': formatted}

    return render(request, 'placedOrder.html', context)
#authentication APIs
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('txt')
        email = request.POST.get('email')
        pswd = request.POST.get('pswd')
        if User.objects.filter(email = email).exists():
            messages.error(request, "email address is already exists")
            return redirect('/')
        if User.objects.filter(username = username).exists():
            messages.error(request, "user name already taken")
            return redirect('/')
        else:
            u = User.objects.create_user(username, email, pswd)
            u.save()
            messages.success(request, "Your account has been created")
            return redirect('/')
    else:
        return HttpResponse('404 notfound')
def handlelogin(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        pswd = request.POST.get('pswd')
        user  = authenticate(username = user_name, password = pswd)
        if user is not None:
            login(request,user)
            messages.success(request, "sucessfully logined")
            return redirect('/')
        else:
            messages.error(request, "Credentials are wrong")
            return redirect('/')
    else:
        return HttpResponse('404 notfound')
def handlellogout(request):
    logout(request)
    messages.success(request, "succesfully logged out")
    return redirect('/')
def search(request):
    query = request.GET.get('search')
    cart_products = CartProduct.objects.filter(cart__user__username=request.user)
    lst = []
    for i in cart_products:
        lst.append(i.product.product_price * i.quantity)
    if gettingCartItem(request.user) == 0:
        total = ""
    else:
        total = gettingCartItem(request.user)
    if query:
        prod = Product.objects.filter(Q(product_name__icontains=query) | Q(product_details__icontains=query))
        # filter products where either the name or details contain the query
    else:
        prod = Product.objects.all()
    context = {'prod':prod, 'query':query, 'totalItem':total}
    return render(request, 'product-list.html', context)
    
        
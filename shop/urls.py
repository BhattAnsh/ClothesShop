from . import views
from django.urls import path

urlpatterns = [
    path("", views.index , name="home"),
    path("product/<int:myid>/", views.productPage , name="ProductPage"),
    path("productList/",views.productList, name="productList"),
    path("post/", views.addToCart, name = 'cart'),
    path("login/", views.handlelogin, name = 'login'),
    path("signup/", views.signup, name = "signup"),
    path("logout/", views.handlellogout, name = "logout"),
    path("search/", views.search, name = "search"),
    path('cart/', views.showCart, name = "showCart"),
    path('cartRemove/', views.removeFromCart, name='removeFromCart'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirmOrder/', views.confirmOrder, name= 'confirmOrder')
]
from django.urls import path
from .import views

urlpatterns = [
path('',views.index, name='home'),
path('login/',views.login_page, name='login'),
path('register/',views.register_page, name='register'),
path('add-cart/<pizza_uid>/',views.add_cart, name='add_cart'),
path('cart/',views.cart, name='cart'),
path('remove_cart_items/<cart_item_uid>/',views.remove_cart_items, name='remove_cart'),
path('orders/',views.order, name='order'),
path('success/',views.success, name='success'),


] 
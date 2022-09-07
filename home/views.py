from urllib import response
from django.shortcuts import render
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.contrib.auth.models import User
# Create your views here.
from instamojo_wrapper import Instamojo
from django.conf import settings

api = Instamojo(api_key=settings.API_KEY,
                auth_token=settings.AUTH_TOKEN,endpoint="https://test.instamojo.com/api/1.1/")

def index(request):
    pizzas=Pizza.objects.all()
    context={
        'pizzas':pizzas
    }
    return render(request,'home.html',context)
def login_page(request):
    if request.method=="POST":
        try:
           username=request.POST.get('username')
           password=request.POST.get('password')
           user_obj=User.objects.filter(username=username)
           if not user_obj.exists():
               messages.warning(request, 'Username not found')
               return redirect('/login/')
            
           if user_obj :=authenticate(username=username,password=password):
             login(request,user_obj)
             return redirect('/')
           messages.error(request, 'Wrong password')
           return redirect('/login/')
        except Exception as e:
           messages.warning(request, 'Something went wrong')
           return redirect('/register/')
    return render(request,'login.html')

    


def register_page(request):
    if request.method=="POST":
        try:
            username=request.POST.get('username')
            email=request.POST.get('email')
            password=request.POST.get('password')

            user_obj=User.objects.filter(username=username,email=email)
            if user_obj.exists():
               messages.warning(request, 'Username or Email is taken')
               return redirect('/register/')
            
            user_obj=User.objects.create(username=username,email=email)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request, 'Account created.')
            return redirect('/login/')
        except Exception as e:
            messages.warning(request, 'Something went wrong')
            return redirect('/register/')
    return render(request, 'register.html')

@login_required(login_url='/login/')
def add_cart(request,pizza_uid):
    user=request.user
    pizza_obj=Pizza.objects.get(uid=pizza_uid)
    cart,_=Cart.objects.get_or_create(user=user,is_paid=False)
    cart_items=Cartitems.objects.create(cart=cart,pizza=pizza_obj)
    return redirect('/')


@login_required(login_url='/login/')
def cart(request):
    cart=Cart.objects.get(is_paid=False, user=request.user)
    response=api.payment_request_create(
      amount=cart.get_cart_total(),
      purpose="Order",
      buyer_name=request.user.username,
      email="shahbaazgudagi0313@gmail.com",
      redirect_url="http://127.0.0.1:8000/success/"
    )
    cart.instamojo_id=response['payment_request']['id']
    cart.save()
    context={'carts':cart,'payment_url':response['payment_request']['longurl']}
 
    
    return render(request,'cart.html',context)


@login_required(login_url='/login/')
def remove_cart_items(request,cart_item_uid):
    try:
       Cartitems.objects.get(uid=cart_item_uid).delete()
       return redirect('/cart/')
    except Exception as e:
       print(e)

@login_required(login_url='/login/')    
def order(request):
    orders=Cart.objects.filter(is_paid=True,user=request.user)
    context={'orders':orders}
    return render(request,'order.html',context)

@login_required(login_url='/login/')
def success(request):
    payment_request=request.GET.get('payment_request_id')
    cart=Cart.objects.get(instamojo_id=payment_request)
    cart.is_paid=True
    cart.save()
    return redirect('/orders/')

        
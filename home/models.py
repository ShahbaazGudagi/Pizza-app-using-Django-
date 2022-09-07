import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
# Create your models here.

class Basemodel(models.Model):
    uid=models.UUIDField(default=uuid.uuid4,editable=False, primary_key=True)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)

    class Meta:
        abstract=True

class PizzaCategory(Basemodel):
    category_name=models.CharField(max_length=100)

    def __str__(self):
        return self.category_name
    


class Pizza(Basemodel):
    category=models.ForeignKey(PizzaCategory,on_delete=models.CASCADE, related_name="pizzas")
    Pizza_name=models.CharField(max_length=100)
    price=models.IntegerField(default=100)
    images=models.ImageField(upload_to="Pizza_image")

    

    def __str__(self) -> str:
        return self.Pizza_name  


class Cart(Basemodel):
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL, related_name="carts")
    is_paid=models.BooleanField(default=False)
    instamojo_id=models.CharField(max_length=1000)
     
     #To sum the total of the Cart
    def get_cart_total(self):
        return Cartitems.objects.filter(cart=self).aggregate(Sum('pizza__price'))['pizza__price__sum']

class Cartitems(Basemodel):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    pizza=models.ForeignKey(Pizza, on_delete=models.CASCADE)






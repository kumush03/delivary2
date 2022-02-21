from django.contrib import admin
from core.models import Category, Customer, FoodCard, Order,Productscart

admin.site.register(Category)
admin.site.register(FoodCard)
admin.site.register(Productscart)
admin.site.register(Order)
admin.site.register(Customer)

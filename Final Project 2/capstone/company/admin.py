from django.contrib import admin
from .models import Product

#Customizing the admin display page
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "nameP", "brand", "price")

# Register your models here.

admin.site.register(Product,ProductAdmin)
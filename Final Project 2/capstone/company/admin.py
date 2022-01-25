from django.contrib import admin
from .models import Product,Supplier

#Customizing the admin display page
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "nameP", "brand", "price")

class SupplierAdmin(admin.ModelAdmin):
    list_display = ("id", "nameS", "contact")

# Register your models here.

admin.site.register(Product,ProductAdmin)
admin.site.register(Supplier,SupplierAdmin)
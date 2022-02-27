from django.contrib import admin
from .models import Product, Supplier, Personnel, Company, Price

#Customizing the admin display page
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "nameP", "brand")

class SupplierAdmin(admin.ModelAdmin):
    list_display = ("id", "nameS", "contact")

class PersonnelAdmin(admin.ModelAdmin):
    list_display = ("id", "nameC", "contact")

class CompanyAdmin(admin.ModelAdmin):
    list_display = ("nameS", "id")

class PriceAdmin(admin.ModelAdmin):
    list_display = ("id", "price", "supplier")
    
# Register your models here.

admin.site.register(Product,ProductAdmin)
admin.site.register(Supplier,SupplierAdmin)
admin.site.register(Personnel,PersonnelAdmin)
admin.site.register(Company,CompanyAdmin)
admin.site.register(Price,PriceAdmin)
from django.contrib import admin
from .models import *

#Customizing the admin display page
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "nameP", "brand")

class SupplierAdmin(admin.ModelAdmin):
    list_display = ("id", "nameC", "contact")

class PersonnelAdmin(admin.ModelAdmin):
    list_display = ("id", "nameC", "contact")

class CompanyAdmin(admin.ModelAdmin):
    list_display = ("nameC", "id")

class PriceAdmin(admin.ModelAdmin):
    list_display = ("id", "price", "supplier")

class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "nameC", "contact")

class JobAdmin(admin.ModelAdmin):
    list_display = ("code", "id", "value", "status")
    
class SupplyAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "qty")

class NotesAdmin(admin.ModelAdmin):
    list_display = ("id", "job", "deliveryNo", "invoiceNo", "receiptNo")

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "password")
    
# Register your models here.

admin.site.register(Product,ProductAdmin)
admin.site.register(Supplier,SupplierAdmin)
admin.site.register(Personnel,PersonnelAdmin)
admin.site.register(Company,CompanyAdmin)
admin.site.register(Price,PriceAdmin)
admin.site.register(Client,ClientAdmin)
admin.site.register(Job,JobAdmin)
admin.site.register(Supply,SupplyAdmin)
admin.site.register(Notes,NotesAdmin)
admin.site.register(User,UserAdmin)
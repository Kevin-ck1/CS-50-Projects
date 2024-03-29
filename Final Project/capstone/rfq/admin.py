from django.contrib import admin

from .models import Supplier, Product, Contact, Zone, Road, Location, Price, Client

class SupplierAdmin(admin.ModelAdmin):
    list_display = ("supplierName","zone", "road", "building", "postal","phoneNumber", "emailSupplier")

class ContactAdmin(admin.ModelAdmin):
    list_display = ("id","name", "supplier", "pNumber", "email", "position")

class ProductAdmin(admin.ModelAdmin):
    list_display =("id","supplierP", "category", "nameP", "brand", "price", "size", "weight", "description")

# class ZoneAdmin(admin.ModelAdmin):
#     list_display =("location")

class RoadAdmin(admin.ModelAdmin):
    list_display = ("roadName", "roadLocation")

class LocationAdmin(admin.ModelAdmin):
    list_display = ("zone1", "road1")

class PriceAdmin(admin.ModelAdmin):
    list_display = ("priceP", "supplierPp", "product")

class ClientAdmin(admin.ModelAdmin):
    list_display = ("clientName", "county", "postal", "clientNumber", "emailClient")

# Register your models here.
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Contact,ContactAdmin)
admin.site.register(Zone)
admin.site.register(Road,RoadAdmin)
admin.site.register(Location,LocationAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Client, ClientAdmin)
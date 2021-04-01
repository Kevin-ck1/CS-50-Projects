from django.contrib import admin

from .models import Supplier, Product, Contact, Zone, Road, Building, Location

class SupplierAdmin(admin.ModelAdmin):
    list_display = ("supplierName","zone", "road", "building", "postal","phoneNumber", "emailSupplier")

class ContactAdmin(admin.ModelAdmin):
    list_display = ("supplier","name", "pNumber", "email", "position")

class ProductAdmin(admin.ModelAdmin):
    list_display =("supplierP", "category", "nameP", "brand", "price", "size", "weight", "description")

# class ZoneAdmin(admin.ModelAdmin):
#     list_display =("location")

class RoadAdmin(admin.ModelAdmin):
    list_display = ("roadName", "roadLocation")

class BuildingAdmin(admin.ModelAdmin):
    list_display = ("buildingName", "broad", "blocation")

class LocationAdmin(admin.ModelAdmin):
    list_display = ("zone1", "road1", "building1")

# Register your models here.
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Contact,ContactAdmin)
admin.site.register(Zone)
admin.site.register(Road,RoadAdmin)
admin.site.register(Building,BuildingAdmin)
admin.site.register(Location,LocationAdmin)
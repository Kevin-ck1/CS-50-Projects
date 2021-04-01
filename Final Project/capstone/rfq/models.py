from django.db import models

# Create your models here.

class Supplier(models.Model):
    supplierName = models.CharField(max_length=64)
    zone = models.IntegerField()
    road = models.IntegerField()
    building = models.IntegerField()
    postal = models.CharField(max_length=64)
    phoneNumber = models.IntegerField()
    emailSupplier = models.CharField(max_length=64)

class Contact(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.SET("Company Deleted"), related_name="supplierC")
    name = models.CharField(max_length=64)
    pNumber = models.IntegerField()
    email = models.CharField(max_length=64)
    position = models.IntegerField()

class Product(models.Model):
    supplierP =  models.ForeignKey(Supplier, on_delete=models.SET("Company Deleted"), related_name="supplierP")
    category = models.IntegerField()
    nameP = models.CharField(max_length=64)
    brand = models.CharField(max_length=64)
    price = models.IntegerField()
    size = models.IntegerField()
    weight = models.IntegerField()
    description = models.TextField()

class Zone(models.Model):
    location = models.CharField(max_length=64)

class Road(models.Model):
    roadName = models.CharField(max_length=64)
    roadLocation = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="zlocation")

class Building(models.Model):
    buildingName = models.CharField(max_length=64)
    broad = models.ForeignKey(Road, on_delete=models.CASCADE, related_name="buildingRoad")
    blocation = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="buildingZone")

class Location(models.Model):
    zone1 = models.CharField(max_length=64)
    road1 = models.CharField(max_length=64)
    building1 = models.CharField(max_length=64)







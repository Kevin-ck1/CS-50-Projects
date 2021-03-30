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
    supplier = models.ForeignKey(Supplier, related_name="supplierC")
    name = models.CharField(max_length=64)
    pNumber = models.IntegerField()
    email = models.CharField(max_length=64)
    position = models.IntegerField()

class Product(models.Model):
    supplierP =  models.ForeignKey(Supplier, related_name="supplierP")
    category = models.IntegerField()
    nameP = models.CharField(max_length=64)
    brand = models.IntegerField()
    price = models.IntegerField()
    size = models.IntegerField()
    weight = models.IntegerField()
    description = models.TextField()






from django.db import models



# Create your models here.

class Product(models.Model):
    #supplierP =  models.ForeignKey(Supplier, on_delete=models.SET("Company Deleted"), related_name="supplierP")
    category = models.IntegerField()
    nameP = models.CharField(max_length=64)
    brand = models.CharField(max_length=64)
    price = models.IntegerField()
    size = models.IntegerField()
    weight = models.IntegerField()
    description = models.TextField()
    supplier = models.IntegerField()

    def __str__(self):
        return f"{self.brand}: {self.nameP}"

class Supplier(models.Model):
    nameS = models.CharField(max_length=64)
    address = models.IntegerField()
    contact = models.IntegerField()
    zone = models.IntegerField()
    location = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.nameS}: {self.contact}"
        

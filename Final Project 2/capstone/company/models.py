from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from polymorphic.models import PolymorphicModel



# Create your models here.

class Company(PolymorphicModel):
    nameS = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.nameS}"

class Supplier(Company):
    address = models.IntegerField()
    email = models.CharField(max_length=64, default=0)
    contact = models.IntegerField()
    zone = models.IntegerField()
    location = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.nameS}: {self.contact}"

class Product(PolymorphicModel):
    category = models.IntegerField()
    nameP = models.CharField(max_length=64)
    brand = models.CharField(max_length=64)
    size = models.IntegerField()
    weight = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f"{self.brand}: {self.nameP}"

class Price(Product):
    productPrice = models.IntegerField()
    #supplier = models.ForeignKey(Supplier,related_name="products", on_delete=models.CASCADE, blank=True, null=True)
    supplier = models.IntegerField()

    def __str__(self):
        return f"{self.productPrice}"

class Personnel(models.Model):
    nameC = models.CharField(max_length=64)
    contact = models.IntegerField()
    email = models.CharField(max_length=64)
    company = models.ForeignKey(Company, related_name="personnel", blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nameC}: {self.contact}"


       

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType



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

class Personnel(models.Model):
    nameC = models.CharField(max_length=64)
    contact = models.IntegerField()
    email = models.CharField(max_length=64)
    content_type = models.ForeignKey(ContentType, related_name="personnel", blank=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return f"{self.nameC}: {self.contact}"

class Supplier(models.Model):
    nameS = models.CharField(max_length=64)
    address = models.IntegerField()
    email = models.CharField(max_length=64, default=0)
    contact = models.IntegerField()
    zone = models.IntegerField()
    location = models.CharField(max_length=64)
    personnel = GenericRelation(Personnel)

    def __str__(self):
        return f"{self.nameS}: {self.contact}"

# >>> from company.models import Personnel
# >>> from company.models import *        
# >>> c1 = Personnel.objects.create(name="kevin", contact="01234", email="kev@gmail.com", content_type="
# s1 = Supplier.objects.get(pk=1)
# >>> c1 = Personnel.objects.create(nameC="kevin", contact="01234", email="kev@gmail.com", content_object=s1)
        

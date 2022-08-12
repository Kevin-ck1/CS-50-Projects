from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from polymorphic.models import PolymorphicModel



# Create your models here.
class Company(PolymorphicModel):
    id = models.BigAutoField(primary_key=True)
    nameC = models.CharField(max_length=64)
    address = models.IntegerField()
    email = models.CharField(max_length=64, default=0)
    contact = models.IntegerField()

    def __str__(self):
        return f"{self.nameC}"

class Supplier(Company):
    zone = models.IntegerField()
    location = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.nameC}"


class Client(Company):
    county = models.IntegerField()
    location = models.CharField(max_length=64)
    

    def __str__(self):
        return f"{self.nameC}"

class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    category = models.IntegerField()
    nameP = models.CharField(max_length=64)
    brand = models.CharField(max_length=64)
    size = models.IntegerField()
    weight = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        productDetails = {
            "nameP":self.nameP, 
            "brand":self.brand,
            "category": self.category
            }
        #return str(productDetails)
        return f"{self.nameP}: {self.brand}"
        

class Price(models.Model):
    id = models.BigAutoField(primary_key=True)
    price = models.IntegerField()
    product = models.ForeignKey(Product, related_name="productPrice",on_delete=models.CASCADE, blank=True, null=True)
    supplier = models.ForeignKey(Supplier,related_name="products", on_delete=models.CASCADE, blank=True, null=True)
    #supplier = models.IntegerField()

    def __str__(self):
        return f"{self.price}"  
 

class Personnel(models.Model):
    id = models.BigAutoField(primary_key=True)
    nameC = models.CharField(max_length=64)
    contact = models.IntegerField()
    email = models.CharField(max_length=64)
    company = models.ForeignKey(Company, related_name="personnel", blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nameC}: {self.contact}"

class Job(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=64)
    client = models.ForeignKey(Client, related_name="client", blank=True, on_delete=models.CASCADE)
    #product = models.ManyToManyField(Product, blank=True, related_name="jobProducts")
    value = models.IntegerField(null=True)
    status = models.CharField(max_length=64, default = "RFQ")
    lpo = models.CharField(max_length=64, blank=True)
    cheque = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f"{self.code}"

class Notes(models.Model):
    id = models.BigAutoField(primary_key=True)
    job = models.ForeignKey(Job, related_name="linkedJob", blank=True, on_delete=models.CASCADE)
    deliveryNo = models.CharField(max_length=64, blank=True)
    invoiceNo = models.CharField(max_length=64, blank=True)
    receiptNo = models.CharField(max_length=64, blank=True) 

    def __str__(self):
        return f"{self.id}: {self.job}: {self.deliveryNo}: {self.invoiceNo} "
    
class Supply(models.Model):
    id = models.BigAutoField(primary_key=True)
    qty = models.IntegerField()
    price = models.IntegerField()
    minBuying =  models.ForeignKey(Price, related_name="bestBuying", on_delete=models.SET_NULL, blank=True, null=True)
    maxBuying =  models.ForeignKey(Price, related_name="worstBuying",on_delete=models.SET_NULL, blank=True, null=True)
    total = models.IntegerField() 
    product = models.ForeignKey(Product, related_name="jobProduct",on_delete=models.CASCADE, blank=True, null=True)
    job = models.ForeignKey(Job, related_name="jobItem",on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.id}: {self.job}" 

       

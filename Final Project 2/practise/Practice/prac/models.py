from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=64)
    qty = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return f"{self.price}"

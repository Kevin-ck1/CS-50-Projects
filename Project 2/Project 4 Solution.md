# Project 4: Solution 

## Step 1 : Migrations

The first step is to make migrations for the auction app

```powershell
python manage.py makemigrations auctions

python manage.py migrate
```





## Step 2: Create the super user

```powershell
python manage.py createsuperuser
```

Where: 

* Username : kevin-admin
* Email:kevin.mutinda.ck@gmail.com
* password : severus321

## Step 3: Create the Models

In the `models.py` 

```python
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    desctiption = models.CharField(max_length=64)
    price = models.IntegerField()
    photo = models.CharField(max_length=64, blank = True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_creator")

    def __str__(self):
        return f"{self.id}: {self.title} {self.desctiption}"

class Bid(models.Model):
    bid_item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_bidder")
    def __str__(self):
        return f"{self.bid_item}"

class Comment(models.Model):
    comment = models.CharField(max_length=64)
    commentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_commentor")

    def __str__(self):
        return f"{self.comment}"
```

Register the created models, in the `admin.py`

```python
from django.contrib import admin

from .models import User, AuctionListing, Bid, Comment

# Register your models here.

admin.site.register(User)
admin.site.register(AuctionListing)
admin.site.register(Bid)
admin.site.register(Comment)
```

Testing that the models are created

```powershell
>> from auctions.models import *
>> AuctionListings.objects.all()
```



## Step 4: Creating Templates

`create.html` for the uploading of the listings

```django

```

## Step 5: Updating the urls

urls.py

```python

```




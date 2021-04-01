# Capstone Project

The app is to use Django in the Backend and vanilla JS in the Front End

So far I expect to have  two projects under the name *capstone*; namely

* rfq
* business
* In case of any other additions, add here

## Step 1: Setting Up Django

Lets start with creating a Django project with the name `capstone`

```shell
django-admin startproject capstone
```

Next , we cd into the `capstone` folder and create the create the `rfq` app, which we are going to start with

```shell
cd capstone

python manage.py startapp rfq
```

Next, we register the `rfq` app in the setting.py file 

```python
INSTALLED_APPS = [
    'rfq', #This is where we add it
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

Next, we configure the url for the new app, first we add the apps default root inside the `capstones` `urls.py` file

Remember to import include.

```python
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rfq.urls')),
]
```

Next, in the `rfq` app we create its `urls.py` file

```python
from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name="index"),
]
```



Next we create the view.py with the function index

```python
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Hello, world")
```

With this if the browser displays the text hello world, the project is set up proparly.

## Step 2: Templates

First we start with the base layout template, where it will contain the navbar(bootstrap) and the link to the style and js script.

Next, we create the index page, for start it will contain forms for submitting data to the database

```django

```



## Step 3: Database

We are to first start with three database to help in functionality of the project.

```python
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
    brand = models.IntegerField()
    price = models.IntegerField()
    size = models.IntegerField()
    weight = models.IntegerField()
    description = models.TextField()
```

Also do facilitate for Django admin Interface we will have to update the `admin.py` file

```python
from django.contrib import admin

from .models import Supplier, Product, Contact

class SupplierAdmin(admin.ModelAdmin):
    list_display = ("supplierName","zone", "road", "building", "postal","phoneNumber", "emailSupplier")

class ContactAdmin(admin.ModelAdmin):
    list_display = ("supplier","name", "pNumber", "email", "position")

class ProductAdmin(admin.ModelAdmin):
    list_display =("supplierP", "category", "nameP", "brand", "price", "size", "weight", "description")
# Register your models here.
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Contact,ContactAdmin)
```

To use the admin page, we will have to create a superuser

```shell
python manage.py createsuperuser
```



## Step 4: Updating views

We update the view to be able to store data from the templates to the data base.
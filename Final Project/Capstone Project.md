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






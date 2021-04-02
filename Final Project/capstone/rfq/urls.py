from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name="index"),
    path('supplierform', views.supplierForm, name="supplierForm"),
    path('contactform', views.contactForm, name="contactForm"),
    path('productform', views.productForm, name="productForm"),
    path('supplier/<int:id>', views.supplierProfile, name="supplierProfile")
]
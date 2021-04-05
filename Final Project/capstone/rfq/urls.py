from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name="index"),
    path('supplierform', views.supplierForm, name="supplierForm"),
    path('contactform', views.contactForm, name="contactForm"),
    path('productform', views.productForm, name="productForm"),
    path('suppliers', views.suppliers, name="suppliers"),
    path('supplier/<int:id>', views.supplierProfile, name="supplierProfile"),
    path('products', views.products, name="products"),
    path('product/<int:id>', views.productProfile, name="productProfile")
]
from . import views
from django.urls import path

app_name = "company"

urlpatterns = [
    path('', views.index, name='index'),
    path('products', views.products, name='products'),
    path('products/search', views.productSearch, name='productSearch'),
    path('productform', views.productForm, name='productForm'),
    path('products/<int:id>', views.productDetail, name='productDetail'),
    path('suppliers', views.suppliers, name='suppliers'),
    path('supplierform', views.supplierForm, name='supplierForm'),
    path('suppliers/<int:id>', views.supplierDetail, name='supplierDetail'),
    path('suppliers/personnel', views.personnel, name="personnel")
   
]

from . import views
from django.urls import path

app_name = "company"

urlpatterns = [
    path('', views.index, name='index'),
    path('fetchItems', views.fetchItems, name='fetchItems'),
    path('products', views.products, name='products'),
    path('productform', views.productForm, name='productForm'),
    path('products/<int:id>', views.productDetail, name='productDetail'),
    path('products/productPrice', views.productPrice, name='productPrice'),
    path('fetchSuppliers', views.fetchSuppliers, name='fetchSuppliers'),
    path('suppliers', views.suppliers, name='suppliers'),
    path('supplierform', views.supplierForm, name='supplierForm'),
    path('suppliers/<int:id>', views.supplierDetail, name='supplierDetail'),
    path('personnel', views.personnel, name="personnel"),
    path('clients', views.clients, name='clients'),
    path('clientform', views.clientForm, name='clientForm'),
    path('clients/<int:id>', views.clientDetail, name='clientDetail'),
    path('jobs', views.jobs, name='jobs'),
    path('jobs/<int:id>', views.jobDetail, name='jobDetail'),
    path('supplies/<int:id>', views.supplies, name='supplies'),
]

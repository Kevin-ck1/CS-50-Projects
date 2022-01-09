from django.shortcuts import render
from . import templates, static
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import Product
import json

# Create your views here.

def index(request):
    return HttpResponse("Hello, World!")

def products(request):
    products = Product.objects.all()
    return render(request, "company/products.html",{
        #To display the products in reverse order, to place the recently added product on top
        "products": products[::-1],
    })

def productForm(request):
    if request.method == "POST":
        data = json.loads(request.body)
        newProduct = data.get("newProduct")
        new_product = Product(**newProduct)
        new_product.save()
        response_data = {
            "message": "Product Stored Successfully.",
            "id": new_product.id
        }
        return JsonResponse(response_data, status=201)

def productDetail(request,id):
    product = Product.objects.get(pk=id)
    return render(request, "company/productdetails.html",{
        "product": product
    })

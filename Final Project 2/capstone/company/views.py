from django.shortcuts import render
from . import templates, static
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import Product, Supplier, Personnel
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
    if request.method == "GET":
        return render(request, "company/productdetails.html",{
        "product": product
    })

    elif request.method == "PUT":
        data = json.loads(request.body)
        editedProduct = data.get("editedProduct")
        product.nameP = editedProduct["nameP"]
        product.brand = editedProduct["brand"]
        product.category = editedProduct["category"]
        product.weight = editedProduct["size"]
        product.size = editedProduct["price"]
        product.description = editedProduct["weight"]
        product.save()

        response_data = {
            "message": "Product Edited Successfully.",
            "id": product.id
        }
        return JsonResponse(response_data, status=201)

    else:
        id = json.loads(request.body)
        Product.objects.get(pk=id).delete()
        
        response_data = {
            "message": "Product Deleted."
        }
        return JsonResponse(response_data, status=201)

def suppliers(request):
    suppliers = Supplier.objects.all()
    return render(request, "company/suppliers.html",{
        "suppliers" : suppliers
    })

def supplierForm(request):
    if request.method == "POST":
        data = json.loads(request.body)
        newSupplier = data.get("newSupplier")
        new_supplier = Supplier(**newSupplier)
        new_supplier.save()
        
        response_data = {
            "message": "Supplier Added.",
            "id": new_supplier.id
        }
        return JsonResponse(response_data, status=201)
    else:
        return render(request, "company/supplierForm.html")

def supplierDetail(request, id):
    supplier = Supplier.objects.get(pk=id)
    personnel = supplier.personnel.all()
    response_data = {
        "supplier": supplier,
        "personnel": personnel
    }
    return render(request, "company/supplierDetails.html", response_data)

def personnel(request):
    if request.method == "POST":
        data = json.loads(request.body)
        person = data.get("newPerson")

        name = person["name"]
        phone = person["phone"]
        email = person["email"]
        companyId = person["companyId"]
        if person["type"] == supplier:
            company = Supplier.objects.get(pk=companyId)
        p = Personnel(nameC = name, contact=phone, email = email, content_object = company)
        p.save()
    response_data ={
        "message": "Personnel Successfully Added"
    }
    return JsonResponse(response_data, status=201)
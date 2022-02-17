from django.shortcuts import render
from . import templates, static
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import Product, Supplier, Personnel, Company, Price
import json

# Create your views here.

def index(request):
    return HttpResponse("Hello, World!")

def products(request):
    products = Product.objects.all()
    suppliers = Supplier.objects.all()
    return render(request, "company/products.html",{
        #To display the products in reverse order, to place the recently added product on top
        "products": products[::-1],
        "suppliers": suppliers
    })

def productForm(request):
    if request.method == "POST":
        rawdata = json.loads(request.body)
        data = rawdata.get("newProduct")
        newProduct = data
        supplierId = int(data["supplier"])
        if supplierId:
            supplier = Supplier.objects.get(pk=supplierId)
            newProduct["supplier"] = supplier
        print(newProduct)
        new_product = Price(**newProduct)
        print(new_product)
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
    zones = ["Zone 1: CBD", "Zone 2: Down Town", "Zone 3: Industrial Area"]
    products = Product.objects.all()

    if request.method == "PUT":
        data = json.loads(request.body)
        ES = data.get("updateSupplier")

        supplier.nameS = ES["nameS"]
        supplier.address = ES["address"]
        supplier.email = ES["email"]
        supplier.contact = ES["contact"]
        supplier.zone = ES["zone"]
        supplier.location = ES["location"]
        supplier.save()

        response_data = {
            "message": "Supplier Edited."
        }
        return JsonResponse(response_data, status=201)

    elif request.method == "DELETE":
        data = json.loads(request.body)
        print(data)
        Id = data.get("supplierId")
        name = data.get("supplierName")
        s = Supplier.objects.get(pk=Id)
        if name == s.nameS:
            s.delete()

            response_data = {
                "message": "Supplier Deleted."
                
            }
            return JsonResponse(response_data, status=201)

    else:
        response_data = {
            "supplier": supplier,
            "personnel": personnel,
            "zones": zones,
            "products": products
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

        if person["type"] == "supplier":
            company = Supplier.objects.get(pk=companyId)
        p = Personnel(nameC = name, contact=phone, email = email, company = company)
        p.save()

        response_data ={
            "message": "Personnel Successfully Added",
            "id": p.id
        }
        return JsonResponse(response_data, status=201)
    
    elif request.method == "PUT":
        data = json.loads(request.body)
        editperson = data.get("updatePerson")
        personId = data.get("personId")
        person = Personnel.objects.get(pk=personId)

        person.nameC = editperson["name"]
        person.contact = editperson["phone"]
        person.email = editperson['email']
        person.save()

        response_data ={
            "message": "Personnel Successfully Updated",
            "id": person.id
        }
        return JsonResponse(response_data, status=201)

    else:
        data = json.loads(request.body)
        personId = data.get("personId")
        Personnel.objects.get(pk=personId).delete()

        response_data ={
            "message": "Personnel Successfully Deleted"
        }
        return JsonResponse(response_data, status=201)




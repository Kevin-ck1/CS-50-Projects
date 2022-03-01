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
    products = Price.objects.all()
    suppliers = Supplier.objects.all()
    categories = ["ICT", "Electricity", "Hairdressing", "Hospitality", "Plumbing & Masonry", "Stationary"]
    return render(request, "company/products.html",{
        #To display the products in reverse order, to place the recently added product on top
        "products": products[::-1],
        "suppliers": suppliers,
        "categories": categories
    })

def productSearch(request):
    products = list(Product.objects.all().values())

    response_data = {
        "products": products
    }
    return JsonResponse(response_data, status=201)

def productForm(request):
    if request.method == "POST":
        #Collecting and Sorting Data
        rawdata = json.loads(request.body)
        newProduct = rawdata.get("newProduct")
        
        supplierId = int(newProduct.pop("supplier", None))
        price = int(newProduct.pop("productPrice", None))

        #Creating New Product
        new_product = Product(**newProduct)
        new_product.save()

        #Creating A price object
        supplier = Supplier.objects.get(pk=supplierId)
        price = Price(price = price, product = new_product , supplier=supplier)
        price.save()

        response_data = {
            "message": "Product Stored Successfully.",
            "id": new_product.id
        }
        return JsonResponse(response_data, status=201)

def productDetail(request,id):
    price = Price.objects.get(pk=id)
    product = price.product
    prices = product.productPrice.all()
    suppliers = Supplier.objects.all()
    
    if request.method == "GET":
        return render(request, "company/productdetails.html",{
            "product": product,
            "prices":prices,
            "suppliers": suppliers
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

def productPrice(request):
    if request.method == "POST":
        data = json.loads(request.body)
        newPrice = data.get("newPrice")
        product = Product.objects.get(pk=newPrice["product"])
        supplier = Supplier.objects.get(pk=newPrice["supplier"])
        price = Price(price = newPrice["price"], product = product , supplier=supplier)
        price.save()
        print(price)
        print(price.id)

        response_data = {
            "message": "Price Added.",
            "id": price.id
        }
        return JsonResponse(response_data, status=201)
    elif request.method == "PUT":
        #Getting updated price
        data = json.loads(request.body)
        editPrice = int(data.get("editPrice"))
        priceId = int(data.get("priceId"))
        
        #Updating the price with the new value
        price = Price.objects.get(pk=priceId)
        price.price = editPrice
        price.save()

        response_data = {
            "message": "Price Edited."
        }
        return JsonResponse(response_data, status=201)

    else:
        #Getting price to delete
        data = json.loads(request.body)
        priceId = int(data.get("priceId"))
        
        #Updating the price with the new value
        price = Price.objects.get(pk=priceId)
        price.delete()

        response_data = {
            "message": "Price Deleted."
        }
        return JsonResponse(response_data, status=201)

def fetchSuppliers(request):
    suppliers = list(Supplier.objects.all().values())
    response_data = {
            "suppliers": suppliers
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




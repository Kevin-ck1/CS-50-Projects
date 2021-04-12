from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from . import templates 
from .models import Supplier, Product, Contact, Zone, Road, Location, Price, Client

# Create your views here.
def index(request):
    return render(request, 'rfq/index.html')

def supplierForm(request):
    if request.method == 'POST':
        mydata = {}
        mydata['supplierName'] = request.POST['supplier-name']
        mydata['zone'] = request.POST['zone']
        mydata['road'] = request.POST['road']
        mydata['building'] = request.POST['building']
        mydata['postal'] = request.POST['postal-address']
        mydata['phoneNumber'] = request.POST['phone-number']
        mydata['emailSupplier'] = request.POST['email-address']

        new_supplier = Supplier(**mydata)
        
        new_supplier.save()

    return HttpResponseRedirect((reverse("supplierProfile", kwargs={"id":1})))

def contactForm(request):
    #Storing Created Contact
    if request.method == "POST":
        data = json.loads(request.body)
        newContact = data.get("newContact")
        new_contact = Contact(**newContact)
        new_contact.save()
        print(new_contact.id)

        response_data = {
            "message": "Contact Stored Successfully.",
            "id":new_contact.id
        }
        return JsonResponse(response_data, status=201)

    #Deleting a Contact
    elif request.method == "DELETE":
        data = json.loads(request.body)
        Contact.objects.get(pk=data).delete()

        return JsonResponse({"message": "Contact Removed"}, status=201)
    

def productForm(request):
    #Storing the a new product
    if request.method == "POST":
        data = json.loads(request.body)
        newProduct = data.get("newProduct")
        print(newProduct)
        new_product = Product(**newProduct)
        new_product.save()

        response_data = {
                "message": "Product Stored Successfully.",
                "id":new_product.id
            }
        return JsonResponse(response_data, status=201)

    #Deleting a product
    elif request.method == "DELETE":
        data = json.loads(request.body)
        Product.objects.get(pk=data).delete()

        return JsonResponse({"message": "Product Removed"}, status=201)

    #Retrieving the product Form
    else:
        suppliers = Supplier.objects.all()
        context = {
            "suppliers": suppliers
        }
        return render(request, "rfq/productForm.html", context)

def suppliers(request):
    suppliers = Supplier.objects.all()
    context = {
        "suppliers": suppliers 
    }
    return render(request, "rfq/supplierList.html", context)


def supplierProfile(request, id):
    supplier = Supplier.objects.get(pk=id)
    contacts = Contact.objects.filter(supplier_id=id).order_by("-id").all()
    products = Product.objects.filter(supplierP_id=id).order_by("-id").all()
    context = {
        "sdetails": supplier,
        "contacts":contacts,
        "products": products
    }
    return render(request, "rfq/supplierDetails.html", context)

def products(request):
    products = Product.objects.all().order_by("-id").all()
    suppliers = Supplier.objects.all()
    context = {
        "products": products,
        "suppliers": suppliers
    }    
    return render(request, "rfq/productList.html", context)

def productProfile(request, id):
    product = Product.objects.get(pk=id)
    context = {
        "product": product
    }

    return render(request, "rfq/productDetail.html", context)

def jobstart(requst):
    products = Product.objects.all()
    return render(requst, "rfq/createRfq.html")

def clients(request):
    if request.method == "POST":
        #Obtaining the posted data for the client
        data = json.loads(request.body)
        client = data.get("newClient")
        #Saving the client details to the database
        new_client = Client(**client)
        new_client.save()

    responsedata = {
        "message": "Product Stored Successfully."
    }
    return JsonResponse(responsedata)
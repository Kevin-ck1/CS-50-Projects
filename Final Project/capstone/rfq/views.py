from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import templates 
from .models import Supplier, Product, Contact, Zone, Road, Location

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
        #Supplier.objects.create(**mydata)
        # new_supplier = Supplier(
        #     supplierName= request.POST['supplier-name'],
        #     zone = request.POST['zone'],
        #     road= request.POST['road'],
        #     building = request.POST['building'],
        #     postal = request.POST['postal-address'],
        #     phoneNumber = request.POST['phone-number'],
        #     emailSupplier = request.POST['email-address']
        # )
        new_supplier.save()

    #return HttpResponseRedirect((reverse("index")))
    return HttpResponseRedirect((reverse("supplierProfile", kwargs={"id":1})))

def contactForm(request):
    if request.method == "POST":
        supplier = Supplier.objects.get(pk=request.POST['supplier'])
        mydata ={}
        #mydata['supplier'] = supplier
        mydata['supplier_id'] = request.POST['supplier']
        mydata['name'] = request.POST['contact-name']
        mydata['pNumber'] = request.POST['contact-phone']
        mydata['email'] = request.POST['contact-email']
        mydata['position'] = request.POST['contact-position']
        new_contact = Contact(**mydata)

        # new_contact = Contact(
        #     supplier = request.POST['supplier'],
        #     name = request.POST['contact-name'],
        #     pNumber = request.POST['contact-phone'],
        #     email = request.POST['contact-email'],
        #     position = request.POST['contact-position']
        # )

        new_contact.save()
        

    return HttpResponseRedirect((reverse("index")))

def productForm(request):
    if request.method == "POST":
        #supplier = Supplier.objects.get(pk=request.POST['supplierP'])
        mydata ={}
        mydata['category'] = request.POST['category']
        mydata['supplierP_id'] =  request.POST['supplierP']
        mydata['nameP'] = request.POST['product-name']
        mydata['brand'] = request.POST['brand']
        mydata['price'] = request.POST['product-price']
        mydata['size'] = request.POST['size']
        mydata['weight'] = request.POST['weight']
        mydata['description'] = request.POST['description']

        new_product = Product(**mydata)

        # new_product = Product(
        #     category =
        #     supplierP =  supplier,
        #     nameP = request.POST['product-name'],
        #     brand = request.POST['brand'],
        #     price = request.POST['product-price'],
        #     size = request.POST['size'],
        #     weight = request.POST['weight'],
        #     description = request.POST['description'] 
        # )
        new_product.save()

    return HttpResponseRedirect((reverse("index")))

def suppliers(request):
    suppliers = Supplier.objects.all()
    context = {
        "suppliers": suppliers 
    }
    return render(request, "rfq/supplierList.html", context)


def supplierProfile(request, id):
    supplier = Supplier.objects.get(pk=id)
    contacts = Contact.objects.filter(supplier_id=id)
    products = Product.objects.filter(supplierP_id=id)
    context = {
        "sdetails": supplier,
        "contacts":contacts,
        "products": products
    }
    return render(request, "rfq/supplierDetails.html", context)

def products(request):
    products = Product.objects.all()

    context = {
        "products": products
    }    
    return render(request, "rfq/productList.html", context)

def productProfile(request, id):
    product = Product.objects.get(pk=id)
    context = {
        "product": product
    }

    return render(request, "rfq/productDetail.html", context)

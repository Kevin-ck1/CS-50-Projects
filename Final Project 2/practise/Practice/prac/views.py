from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
import csv

# Create your views here.
def index(request):
    #return HttpResponse("Hello, World")
    return render(request, "index.html")

def print_excel(request):
    products = Product.objects.all()
    print(products)
    print("Hello World")

    return render(request, "index.html")

def print_csv(request):
    products = Product.objects.all()
    print(products)
    print("Hello World")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename = products.csv'
    writer = csv.writer(response)
    writer.writerow(['Name', "QTY", "Price"])
    for p in products:
        writer.writerow([p.name, p.qty, p.price])

    return response
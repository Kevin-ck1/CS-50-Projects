from django.shortcuts import render
from . import templates, static
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, FileResponse
from .models import Product, Supplier, Personnel, Company, Price, Client, Job, Supply
import json
from django.db.models import Avg, Max, Min, Sum
from itertools import chain
from django.db.models import Subquery, OuterRef, FloatField, CharField
from django.db.models.functions import Cast
import pandas as pd
import csv, io, xlsxwriter, xlwt
from capstone.settings import EMAIL_HOST_USER

#Common variables
categories = ["ICT", "Electricity", "Hairdressing", "Hospitality", "Plumbing & Masonry", "Stationary"]
counties = ['Mombasa', 'Kwale', 'Kilifi', 'Tana', 
'River', 'Lamu', 'Taita', 'Mak', 'Taveta', 'Garissa', 'Wajir', 
'Mandera', 'Marsabit', 'Isiolo', 'Meru', 'Tharaka-Nithi', 'Embu', 'Kitui', 
'Machakos', 'Makueni', 'Nyandarua', 'Nyeri', 'Kirinyaga', 'Murang’a', 
'Kiambu', 'The', 'Turkana', 'West', 'Pokot', 'Samburu', 'Trans-Nzoia', 
'Uasin', 'Gishu', 'Elgeyo-Marakwet', 'Nandi', 'Baringo', 'Laikipia', 'Nakuru',
 'Narok', 'Kajiado', 'Kericho', 'Bomet', 'Kakamega', 'Vihiga', 'Bungoma', 
 'Busia', 'Siaya', 'Kisumu', 'Homa', 'Bay', 'Migori', 'Kisii', 'Nyamira', 
 'Nairobi']
status = ["RFQ", "LPO", "Supplied", "Paid"] 

# Create your views here.

def index(request):
    return HttpResponse("Hello, World!")

def products(request):
    products = Price.objects.all()
    suppliers = Supplier.objects.all()
    
    return render(request, "company/products.html",{
        #To display the products in reverse order, to place the recently added product on top
        "products": products[::-1],
        "suppliers": suppliers,
        "categories": categories
    })

def fetchItems(request):
    products = list(Product.objects.all().values())
    suppliers = list(Supplier.objects.all().values())
    jobs = list(Job.objects.all().values())
    prices = list(Price.objects.all().values())

    response_data = {
        "products": products,
        "suppliers": suppliers,
        "jobs": jobs,
        "prices": prices
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
    products = Product.objects.all()
    if products.filter(pk=id).exists():
        product = Product.objects.get(pk=id)
        prices = product.productPrice.all()
        suppliers = Supplier.objects.all()
        
        if request.method == "GET":
            return render(request, "company/productdetails.html",{
                "product": product,
                "prices":prices,
                "suppliers": suppliers,
                "categories": categories
            })

        elif request.method == "PUT":
            data = json.loads(request.body)
            editedProduct = data.get("editedProduct")
            product.nameP = editedProduct["nameP"]
            product.brand = editedProduct["brand"]
            product.category = editedProduct["category"]
            product.weight = editedProduct["weight"]
            product.size = editedProduct["size"]
            product.description = editedProduct["description"]
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
    else:
        return HttpResponse("Product Does Not exist")

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
        #Getting data from json
        data = json.loads(request.body)
        priceId = int(data.get("priceId"))
        
        #Getting the price to delete
        price = Price.objects.get(pk=priceId)
        product = price.product
        prices = product.productPrice.all()
        if prices.count()  > 1:
            price.delete()

            response_data = {
                "message": 1
            }
            return JsonResponse(response_data, status=201)
        else:
            response_data = {
                "message": 0
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
        newSupplier = data.get("newCompany")
        newSupplier.pop("county")
        new_supplier = Supplier(**newSupplier)
        new_supplier.save()
        print(new_supplier)
        
        response_data = {
            "message": "Supplier Added.",
            "id": new_supplier.id
        }
        return JsonResponse(response_data, status=201)
    else:
        return render(request, "company/companyForm.html", {
            "mode": "Supplier",
        })

def supplierDetail(request, id):
    supplier = Supplier.objects.get(pk=id)
    personnel = supplier.personnel.all()
    zones = ["Zone 1: CBD", "Zone 2: Down Town", "Zone 3: Industrial Area"]
    products = Price.objects.all()

    if request.method == "PUT":
        data = json.loads(request.body)
        ES = data.get("updateCompany")

        supplier.nameC = ES["nameC"]
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
        supplier.delete()

        response_data = {
            "message": "Supplier Deleted."
                
        }
        return JsonResponse(response_data, status=201)

    else:
        context = {
            "supplier": supplier,
            "personnel": personnel,
            "zones": zones,
            "products": products
        }

        return render(request, "company/supplierDetails.html", context)

    

def personnel(request):
    if request.method == "POST":
        data = json.loads(request.body)
        person = data.get("newPerson")

        name = person["name"]
        phone = person["phone"]
        email = person["email"]
        companyId = person["companyId"]

        company = Company.objects.get(pk=companyId)

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


def clients(request):
    clients = Client.objects.all()
    return render(request, "company/clients.html",{
        "clients": clients
    })


def clientForm(request):
    if request.method == "POST":
        data = json.loads(request.body)
        newClient = data.get("newCompany")
        newClient.pop("zone")
        new_Client = Client(**newClient)
        new_Client.save()
        
        response_data = {
            "message": "ClientAdded.",
            "id": new_Client.id
        }
        
        return JsonResponse(response_data, status=201)
    else:
        return render(request, "company/companyForm.html", {
            "mode": "Client",
            "counties": counties
        })

def clientDetail(request, id):
    client = Client.objects.get(pk=id)
    personnel = client.personnel.all()
    jobs = client.client.all()
    # jobs = [{"code":"job1", "value":10000, "status":"RFQ"},
    # {"code":"job2", "value":"25000", "status":"LPO"}
    # ]

    if request.method == "PUT":
        data = json.loads(request.body)
        editDetails = data.get("updateCompany")
        client.nameC = editDetails["nameC"]
        client.address = editDetails["address"]
        client.email = editDetails["email"]
        client.contact = editDetails["contact"]
        client.county = editDetails["county"]
        client.location = editDetails["location"]
        client.save()

        response_data = {
            "message": "Client Edited."
        }
        return JsonResponse(response_data, status=201)
    
    elif request.method == "DELETE":
        client.delete()

        response_data = {
            "message": "Client Deleted."
        }
        return JsonResponse(response_data, status=201)

    context = {
        "client": client,
        "personnel": personnel,
        "counties": counties,
        "jobs": jobs
    }

    return render(request, "company/clientDetails.html", context)

def jobs(request):
    if request.method == "POST":
        data = json.loads(request.body)
        j = data.get("newJob")
        client = Client.objects.get(pk = j["client"] )
        newJob = Job(code = j["code"], client = client)
        newJob.save()

        return JsonResponse({"message": "Job Added"}, status=201)
    

    jobs = Job.objects.all()
    products = Price.objects.all()
    suppliers = Supplier.objects.all()
    clients = Client.objects.all()

    context = {
        "jobs": jobs[::-1],
        "products": products[::-1],
        "suppliers": suppliers,
        "clients": clients,
    }

    return render(request, "company/jobs.html", context)

def jobDetail(request, id):
    job = Job.objects.get(pk=id)
    supplies = job.jobItem.all()
    
    #products = Product.objects.all()
    #products = job.product.all()
    #products = Price.objects.all()


    if request.method == "DELETE":
        job.delete()

        return JsonResponse({"message": "Job Deleted"}, status = 201)
    elif request.method == "PUT":
        data = json.loads(request.body)
        job.status = data.get("status")
        job.save()
        return JsonResponse({"message": "Status Updated"}, status = 201)

    context = {
        "job": job, 
        "status": status,
        "supplies": supplies,
    }

    return render(request, "company/jobDetails.html", context)

def supplies(request, id):
    if request.method == "POST":
        data = json.loads(request.body)
        newSupply = data.get("newSupply")
        print(newSupply)

        product = Product.objects.get(pk = newSupply["product"])
        #Getting the min and max prices
        prices = Price.objects.filter(product = product)
        #minPrice = prices.aggregate(Min('price'))["price__min"]
        #maxPrice = prices.aggregate(Max('price'))["price__min"]
        # minBuying = prices.get(price = minPrice)
        # maxBuying = prices.get(price = maxPrice)
        minBuying = prices.get(price = newSupply['minPrice'])
        maxBuying = prices.get(price = newSupply['maxPrice'])

        #Fetching the job instace
        job = Job.objects.get(pk = newSupply["job"] )

        new_supply = Supply(
            id = newSupply["product"],
            qty = newSupply["qty"],
            price = newSupply["price"],
            minBuying = minBuying,
            maxBuying = maxBuying,
            total = newSupply["total"],
            product = product,
            job = job,
        )
        new_supply.save()
        print(new_supply)

        #Updating the job value
        updateJobValue(job)

        response_data = {
            "message": "Supply Added.",
            "jobValue": job.value
        }
        return JsonResponse(response_data, status=201)    

    elif request.method == "PUT":
        data = json.loads(request.body)
        editedSupply = data.get("editedSupply")
        s = Supply.objects.get(pk=editedSupply["id"])
        s.qty = editedSupply['qty']
        s.price = editedSupply['price']
        s.total = editedSupply['total']
        s.save()

        #Update the jobvalue after edit
        updateJobValue(s.job)

        response_data = {
            "message": "Supply Edited."
        }
        return JsonResponse(response_data, status=201)

    else:
        s = Supply.objects.get(pk=id)
        s.delete()

        #Update the job value after delete
        updateJobValue(s.job)

        response_data = {
            "message": "Supply Deleted."
        }
        return JsonResponse(response_data, status=201)


def updateJobValue(job):
    supplies = job.jobItem.all()
    jobValue = supplies.aggregate(Sum('total'))['total__sum']
    job.value = jobValue
    job.save()
    print("Testing value save")
    print(job)
    print(job.value)
    print("End of value save")

def getItems(request, type, id):
    job = Job.objects.get(pk=id)
    products = Product.objects.all()
    supplies = job.jobItem.all()
    #Join Code
    subquery = products.filter(id=OuterRef('product_id'))
    combined = supplies.annotate(
        category = Cast(Subquery(subquery.values('category')[:1]), output_field=FloatField()),
        nameP = Cast(Subquery(subquery_p.values('nameP')[:1]), output_field=CharField()),
        brand = Cast(Subquery(subquery_p.values('brand')[:1]), output_field=CharField()),
        buying = Cast(Subquery(subquery_buying.values('price')[:1]), output_field=CharField()),
        supplier = Cast(Subquery(subquery_buying.values('supplier')[:1]), output_field=CharField()),
    )

    print(combined.values())

    df = pd.DataFrame(list(combined.values()))
    print(df.head())
    #df.to_excel('Supplies.xlsx')
    print(list(supplies.values()))

    # Create the HttpResponse object with the appropriate CSV header.
    if type == "print_csv":
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename = products.csv'

        rows = list(combined.values())
        writer = csv.writer(response)
        writer.writerow(["qty", "price", "total"])
        
        for row in rows:
            #writer.writerow([s.qty, s.price, s.total])
            writer.writerow([row['qty'], row['price'], row["product_id"]])
        return response
    
    elif type == "print_excel":
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename = products.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Products')
        
        # Sheet header, first row
        row_num = 0
        #Setting the fonts for Headings
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        #Naming the Column Heads for products
        columns = ['nameP', 'brand', 'category', ]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle() #Removing the bold from the font

        rows = Product.objects.all().values_list('nameP', 'brand', 'category')
        print(rows)
        for row in rows:
            print(f"Test 2{type (row)}")
            print(row)
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response

    #Printing Excel using pd
        # excel_file = io.BytesIO()
        # xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')
        # df.to_excel(xlwriter, 'sheetname')
        # xlwriter.save()
        # #xlwriter.close()
        # excel_file.seek(0)

        # response = HttpResponse(excel_file.read(), content_type='application/ms-excel')
        # # set the file name in the Content-Disposition header
        # response['Content-Disposition'] = 'attachment; filename=myfile.xls'
        # return response    
    elif type == "print_rfq":
       # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename = supplies.csv'
        writer = csv.writer(response)
        writer.writerow(["qty", "price", "total"])
        
        for s in supplies:
            writer.writerow([s.qty, s.price, s.total])
        return response 

        #To excel using pandas
        writer = pd.ExcelWriter('test_file.xlsx') 
        df.to_excel(writer, sheet_name='my_analysis', index=False, na_rep='NaN')

        # Manually adjust the width of the last column
        writer.sheets['my_analysis'].set_column(3, 3, 45)

        writer.save()
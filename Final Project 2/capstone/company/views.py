from django.shortcuts import render
from . import templates, static, util
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, FileResponse
from django.shortcuts import redirect
from .models import *
import json
from django.db.models import Avg, Max, Min, Sum
from itertools import chain
from django.db.models import Subquery, OuterRef, FloatField, CharField, IntegerField
from django.db.models.functions import Cast
import pandas as pd
import csv, io, xlsxwriter, xlwt, math
from reportlab.pdfgen import canvas
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from xhtml2pdf import pisa
from capstone.settings import EMAIL_HOST_USER
from django.contrib import messages
from wkhtmltopdf.views import PDFTemplateResponse 
import os
from datetime import date, datetime
from django.core.paginator import Paginator

#os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\bin")
from weasyprint import HTML, CSS
from django.template.loader import get_template, render_to_string
from django.core.files.storage import FileSystemStorage

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

def login_view(request):
    return render(request, "company/login.html")

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

        #Updating the corresponding supply items if any
        updateSupplies(price)
        

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

        #Updating the corresponding supply items if any
        updateSupplies(price)

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
            #Updating the corresponding supply items if any
            updateSupplies(price)
            #Deleting the price
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

def updateSupplies(price):
    product = price.product
    supplies = product.jobProduct.all()
    if supplies.exists():
        for s in supplies:
            job = s.job
            if job.status == "RFQ":
                prices = Price.objects.filter(product = product)
                minPrice = prices.aggregate(Min('price'))["price__min"]
                maxPrice = prices.aggregate(Max('price'))["price__max"]
                s.minBuying = prices.get(price = minPrice)
                s.maxBuying = prices.get(price = maxPrice)  
                s.price = (math.ceil(maxPrice*1.36/5))*5 
                s.total = s.price * s.qty
                s.save()
                #Updating the job value
                updateJobValue(job)

def fetchSuppliers(request):
    suppliers = list(Supplier.objects.all().values())
    response_data = {
            "suppliers": suppliers
        }
    return JsonResponse(response_data, status=201)

def suppliers(request):
    suppliers = Supplier.objects.all()

    #Paginating the suppliers
    paginator = Paginator(suppliers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "company/suppliers.html",{
        # "suppliers" : suppliers
        "suppliers" : page_obj
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

        response_data = {
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
    #Paginating the clients
    paginator = Paginator(clients, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "company/clients.html",{
        "clients": page_obj
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

    if request.method == "DELETE":
        job.delete()

        return JsonResponse({"message": "Job Deleted"}, status = 201)
    elif request.method == "PUT":
        data = json.loads(request.body)
        updated_status = data.get("status")
        current_status = job.status
        if status.index(str(updated_status)) > status.index(str(current_status)):
            job.status = updated_status
            job.save()
        return JsonResponse({"message": "Status Updated"}, status = 201)

    # if "message" not in request.session:
    #     request.session['message'] = ''
    # message = request.session['message']

    elif request.method == "POST":
        data = json.loads(request.body).get("data")
        value = data["value"]

        if data["type"] == "cheque":
            job.cheque = value
            job.save()
        else:
            job.lpo = value
            
            job.save()

            #Generating the notes 
            notes = Notes.objects.all()
            x = datetime.now()
            y = x.strftime("/%m/%Y")

            if notes:
                if not notes.filter(job = job).exists() :
                    last = notes.last()
                    sub1 = last.deliveryNo[3:-2]
                    if y == sub1:
                        sub2 = int(last.deliveryNo[-1]) + 1
                    else:
                        sub2 = 1
                    util.create_notes(job, y, sub2)
            else:
                util.create_notes(job, y, 1)

        return JsonResponse({"message": "Data Saved"}, status = 201)

    context = {
        "job": job, 
        "status": status,
        "supplies": supplies,
        #"message": message
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
        s = Supply.objects.get(id=editedSupply["id"])
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
        s = Supply.objects.get(id=id)
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
    job.value = jobValue if jobValue is not None else 0
    job.save()

def getItems(request, type, id):
    job = Job.objects.get(pk=id)
    products = Product.objects.all()
    supplies = job.jobItem.all()

    #Variables to render to the html page
    context = {
        "job": job, 
        #"status": status,
        "supplies": supplies,
    }

    #Joining the subqueries
    subquery1 = products.filter(id=OuterRef('product_id'))
    subquery2 = Price.objects.all().filter(id=OuterRef('minBuying_id'))
    combined = supplies.annotate(
        category = Cast(Subquery(subquery1.values('category')[:1]), output_field=IntegerField()),
        nameP = Cast(Subquery(subquery1.values('nameP')[:1]), output_field=CharField()),
        brand = Cast(Subquery(subquery1.values('brand')[:1]), output_field=CharField()),
        buying = Cast(Subquery(subquery2.values('price')[:1]), output_field=IntegerField()),
        supplier = Cast(Subquery(subquery2.values('supplier')[:1]), output_field=IntegerField()),
        bt = (Cast('qty',output_field=IntegerField()) * Cast('buying',output_field=IntegerField())),
    )

    if type == "print_rfq_csv":
       # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename = {job.code}.csv'
        writer = csv.writer(response)
        writer.writerow(["Product","brand","qty", "Buying","Selling", "Buying total", "Selling Total"])
        total_buying = 0
        total_selling = 0
        for s in supplies:
            writer.writerow([s.product.nameP, s.product.brand, s.qty, s.minBuying.price, s.price,(s.minBuying.price*s.qty), s.total])
            total_buying += (s.minBuying.price*s.qty)
            total_selling += s.total
        writer.writerow(["","","","","Grand Total", total_buying, total_selling, "Difference",(total_selling-total_buying)])
        return response 

    elif type == "check_analysis":
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename = {job.code}.xlsx'

        columns_heads = ["Product","brand","qty", "Buying","Selling", "Buying total", "Selling Total"]
        rows = combined.values_list('nameP', 'brand', 'qty', 'buying', 'price', 'bt', 'total')

        output = util.create_xlsx(combined, columns_heads, rows)
        
        response.write(output.getvalue())

        return response

    elif type == "invoice_request":
        
        suppliers_list = combined.values_list('supplier', flat=True).distinct() #This gives a value to get an object remove flat=True
        
        print(suppliers_list)
        for i in suppliers_list:
            print(i)
            supplier = Supplier.objects.filter(id=i)
            items = combined.filter(supplier = (i))  
            columns_heads = ["Product","brand","qty", "Total","Price"]
            rows = combined.values_list('nameP', 'brand', 'qty')

            output = util.create_xlsx(items, columns_heads, rows)

            #Sending mail
            subject, from_email, to = 'Django Test', EMAIL_HOST_USER, supplier.values_list('email', flat=True)[0]
            text_content = 'Could you kindly furnish us with an invoice of the attached items.'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach('supplies.xlsx',output.getvalue(), 'application/vnd.ms-excel')
            msg.send()

        messages.success(request, 'Email Sent.')
        #request.session['message'] = "Invoice Request Sent"

        #return render (request, "company/jobDetails.html", context)
        #return HttpResponseRedirect(reverse("company:jobDetail", args=(id,)))
        #return HttpResponseRedirect(reverse("company:jobDetail", kwargs={'id':id}))
        return redirect(reverse("company:jobDetail", kwargs={'id':id}))

    elif type == "print_rfq_pdf":

        a = [{"title":"RFQ", "body":"Quotation for RFQ"}]
        response = util.create_pdf(context, a)
        return response
        
        # template = get_template(template_path)
        # html = template.render(context)

        # result = io.BytesIO()
        # #Creating the pdf
        # output = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result, encoding='UTF-8')

        # if not output.err:
        #     pdf = HttpResponse(result.getvalue(), content_type='application/pdf')
        #     #pdf['Content-Disposition'] = f'attachent; filename = "{job.code}.pdf"'
        #     return pdf  
        # return None   
        # 
        # cmd = [
        #   settings.WKHTMLTOPDF_CMD,
        #   '--page-size', 'A4', '--encoding', 'utf-8',
        #   '--footer-center', '[page] / [topage]',
        #   '--enable-local-file-access']       

        # response = PDFTemplateResponse (
        #     request=request,
        #     template=template_path,
        #     filename ="Test.pdf",
        #     context=context,
        #     show_content_in_browser=False,
        #     cmd_options={'margin-top': 50,}
        # )

        # html_template = get_template(template_path)
        # html_string = render_to_string(template_path, context)
        # pdf_file = HTML(string=html_string).write_pdf(
        #     stylesheets = [CSS("company/static/company/styles.css"),
        #         CSS("company/static/company/styles_print.css")
        #     ]
        # ) 
        # response = HttpResponse(pdf_file, content_type='application/pdf')
        # response['Content-Disposition'] = f'attachent; filename = "{job.code}.pdf"'
        # return response

        #Saving to a virtual file
        # result = io.BytesIO()
        # pdf_file = HTML(string=html_string).write_pdf(result)
        # # result.seek()

        # from puppeteer_pdf import render_pdf_from_template

        # pdf = render_pdf_from_template(
        #     input_template= template_path,
        #     header_template='',
        #     footer_template='',
        #     context=context,
        #     cmd_options={
        #         'format': 'A4',
        #         'scale': '1',
        #         'marginTop': '0',
        #         'marginLeft': '0',
        #         'marginRight': '0',
        #         'marginBottom': '0',
        #         'printBackground': True,
        #         'preferCSSPageSize': True,
        #         #'output': output_temp_file,
        #         'pageRanges': 1
        #     }
        # )

        # response = HttpResponse(pdf, content_type='application/pdf')
        # response['Content-Disposition'] = f'attachent; filename = "{job.code}.pdf"'
        # return response

    elif type == "print_DI":
        a = [{"title":"Invoice", "body":"Invoice"}, {"title":"Delivery", "body":"Delivery Note"}]
        response = util.create_pdf(context, a)
        return response

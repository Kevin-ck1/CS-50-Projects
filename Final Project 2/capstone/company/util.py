import csv, io, xlsxwriter, xlwt, math
from datetime import date, datetime
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, FileResponse
from weasyprint import HTML, CSS
from django.template.loader import get_template, render_to_string
from PyPDF2 import PdfFileMerger
from .models import *
import pandas as pd

def create_xlsx(combined, columns_heads, rows):
    #Creating the Spreadsheat, in memorry with io
    output = io.BytesIO()
    wb = xlsxwriter.Workbook(output)
    ws = wb.add_worksheet()


    # Sheet header, first row
    row_num = 0

    # Add a bold format to use to highlight cells.
    bold = wb.add_format({'bold': True})

    #Naming the Column Heads for products
    columns = columns_heads

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], bold)
        ws.set_column(col_num, col_num,12)

    #rows = combined.values_list('nameP', 'brand', 'qty', 'buying', 'price', 'bt', 'total')
        
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num])    

    wb.close()

    return output

def create_pdf(context, a):
    job = context["job"]
    template_path = "company/print.html"
    x = datetime.now()
    context["date"] = x.strftime(" %d/%m/%Y")
    pdfs = []
    for i in a:
        context["type"] = i
        html_template = get_template(template_path)
        html_string = render_to_string(template_path, context)

        pdf = HTML(string=html_string).write_pdf(
            stylesheets = [CSS("company/static/company/styles.css"),
                CSS("company/static/company/styles_print.css")
            ]
        ) 

        pdf_buffer = io.BytesIO(pdf)

        pdfs.append(pdf_buffer)
    
    pdf_merger = PdfFileMerger()

    for pdf in pdfs:
        pdf_merger.append(pdf)

    buffer = io.BytesIO()
    pdf_merger.write(buffer)

    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename = "Delivery:{job.code}.pdf"'
    return response

def create_notes(job,y,sub):
    n = Notes(
            job = job, 
            deliveryNo = f"Del{y}-{sub}",
            invoiceNo = f"Inv{y}-{sub}", 
            receiptNo = f"Rec{y}-{sub}"
        ) 
    n.save()

def get_counties():
    df = pd.read_excel('company/static/company/data/data.xlsx', sheet_name='Counties')
    counties = df['County'].tolist()
    return counties

def get_categories():
    df = pd.read_excel('company/static/company/data/data.xlsx', sheet_name='Categories')
    a = df['CATEGORIES'].tolist()
    return a

def get_status():
    df = pd.read_excel('company/static/company/data/data.xlsx', sheet_name='Status')
    a = df['STATUS'].tolist()
    return a

def get_zones():
    df = pd.read_excel('company/static/company/data/data.xlsx', sheet_name='Zones')
    a = df['ZONES'].tolist()
    return a

def get_data():
    def data(a, b):
        df = pd.read_excel('company/static/company/data/data.xlsx', sheet_name=a)
        c = df[b].tolist()
        return c
    data1 = {"Counties":data('Counties', 'County'), "Categories":data('Categories', 'CATEGORIES'), "Status":data('Status', 'STATUS'), "Zones":data('Zones', 'ZONES')}

    # print(data1)
    # import json
    # #j1 = json.loads(data1)

    # j2 = json.dumps(data2)
    # j1 = json.loads(j2)
    # print("Below is data convert from json")
    # print((j1))
    # print("Below is json data")
    # print(j2)
    return data1

def get_county():
    df = pd.read_excel('company/static/company/data/data.xlsx', sheet_name= "Counties")
    a = df.to_dict('records')
    return a

def supply_factor(product, job):
    counties_dict = get_county()
    county = counties_dict[(job.client.county) - 1]
    distance = county['Distance(km)']
    weight = (product.weight)/1000

    factor = 1+(distance/806)+(0.16+0.1)+(weight)
    print(factor)

    return factor

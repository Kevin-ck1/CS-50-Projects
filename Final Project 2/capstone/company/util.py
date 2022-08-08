import csv, io, xlsxwriter, xlwt, math
from datetime import date, datetime
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, FileResponse
from weasyprint import HTML, CSS
from django.template.loader import get_template, render_to_string
from PyPDF2 import PdfFileMerger

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
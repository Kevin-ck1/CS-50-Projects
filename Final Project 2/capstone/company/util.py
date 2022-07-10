import csv, io, xlsxwriter, xlwt, math

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
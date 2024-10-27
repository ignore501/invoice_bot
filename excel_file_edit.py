import openpyxl

from openpyxl.styles import Font
from vars import invoice_templates
from data_formatting import (date_to_string,
                             base_to_string,
                             subtotal_string,
                             total_string_in_letters,
                             price_format)


def make_invoice(data: list):
    if len(data) == 7:
        filename = invoice_templates[data[0]]

        wb = openpyxl.load_workbook(f'templates/{filename}.xlsx')
        sheet = wb.active
        sheet['B10'] = date_to_string(data[1])
        sheet['G16'] = data[2]
        sheet['G17'] = f'ИНН {data[3]}'
        sheet['G19'] = base_to_string(data[4])
        sheet['D22'] = data[5]
        sheet['AF22'] = sheet['AK22'] = sheet['AL26'] =\
            price_format(data[6]) + ' ₽'
        sheet['AL26'].font = Font(bold=True)
        sheet['B29'] = subtotal_string(data[6])
        sheet['B30'] = total_string_in_letters(data[6])
        sheet['B30'].font = Font(bold=True)

        wb.save(f'templates/{filename}.xlsx')

        return filename

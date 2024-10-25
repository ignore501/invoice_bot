import openpyxl
from number_to_string import get_string_by_number
from openpyxl.styles import Font
from vars import list_of_months, invoice_templates


def date_to_string(d: str):     # на вход дата строка 17.12.1987,
    date_list = d.split('.')    # строка с номером счета и датой на выход
    months_list = list_of_months
    main_string = f'Счет на оплату № 1.{d}-C от {int(date_list[0])} {
        months_list[int(date_list[1])]} {int(date_list[-1])} г.'
    return main_string


def base_to_string(b: str):     # на вход номер договора 1.21/12/24,
    months_list = list_of_months
    number = b[0]
    b_string = b[2::]
    b_string = b_string.split('/')
    base_string = f'Договор № {number}.{b_string[0]}/{b_string[1]}/{
        b_string[2]} от {b_string[0]} {months_list[int(b_string[1])]} 20{
            b_string[2]} г.'
    return base_string      # строка основание на выход


def subtotal_string(n: str):
    n = n.split('.')
    x = '{0:,}'.format(int(n[0])).replace(',', ' ')
    subtotal = f'Всего наименований 1, на сумму {x},{n[1]} руб.'
    return subtotal     # форматируем строку в денежный формат


def total_string_in_letters(n: str):
    string = get_string_by_number(float(n))
    return string


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
        sheet['AF22'] = sheet['AK22'] = sheet['AL26'] = float(data[6])
        sheet['AL26'].font = Font(bold=True)
        sheet['B29'] = subtotal_string(data[6])
        sheet['B30'] = total_string_in_letters(data[6])
        sheet['B30'].font = Font(bold=True)

        wb.save(f'templates/{filename}.xlsx')

        return filename


# data = ["Т-БИЗНЕС",
#         "12.11.2122",
#         "Тестовая организация",
#         "1234567",
#         "1.10/12/23",
#         "Производство наладочных работ",
#         "21233554.19"]
# make_invoice(data=data)

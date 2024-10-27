from vars import list_of_months
from number_to_string import get_string_by_number


def date_to_string(d: str):     # на вход дата строка 17.12.1987,
    date_list = d.split('.')    # строка с номером счета и датой на выход
    if len(date_list[0]) < 2:
        date_list[0] = '0' + date_list
    main_string = f'Счет на оплату № 1.{d}-C от {int(date_list[0])} {
        list_of_months[int(date_list[1])]} {int(date_list[-1])} г.'
    return main_string


def base_to_string(base: str):     # на вход номер договора 1.21/12/24,
    base_date = base.replace('/', '.').split('.')
    base_string = f'Договор № {base} от {base_date[1]} {
        list_of_months[int(base_date[1])]} 20{base_date[2]} г.'
    return base_string      # строка основание на выход


def price_format(price: str):
    price = price.replace(',', '.')
    price = "{:.2f}".format(float(price))
    price = price.split('.')
    price = f'{'{0:,}'.format(int(price[0])).replace(',', ' ')}.{price[1]}'
    return price


def subtotal_string(n: str):
    x = price_format(n)
    x = x.split('.')
    subtotal = f'Всего наименований 1, на сумму {x[0]},{x[1]} руб.'
    return subtotal     # форматируем строку в денежный формат


def total_string_in_letters(n: str):
    n = n.replace(',', '.')
    string = get_string_by_number(float(n))
    return string

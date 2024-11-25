from decimal import Decimal
import datetime

goods = dict()
DATE_FORMAT = "%Y-%m-%d"


def add(items, title, amount, expiration_date=None):
    if expiration_date is None:
        date = None
    else:
        date = datetime.datetime.strptime(expiration_date, DATE_FORMAT)
        date = date.date()
    product_dict = {"amount": Decimal(amount), "expiration_date": date}
    if title in items:
        intermediate_list = items[title].copy()
        intermediate_list.append(product_dict)
        items[title] = intermediate_list
    else:
        items[title] = [product_dict]


def add_by_note(items, note):
    note_list = note.split()
    if note_list[-1].count("-") == 2:
        expiration_date = note_list[-1]
        amount = note_list[-2]
        title = " ".join(note_list[:-2])
        add(items, title, amount, expiration_date)
    else:
        amount = note_list[-1]
        title = " ".join(note_list[:-1])
        add(items, title, amount)


def find(items, needle):
    total_list = []
    for key in items:
        if needle.lower() in key.lower():
            total_list.append(key)
    return total_list


def amount(items, needle):
    list_found_products = find(items, needle)
    quantity = Decimal(0)
    for product in list_found_products:
        for selected_product in items[product]:
            quantity += selected_product["amount"]
    return quantity


def expire(items, in_advance_days=0):
    list_expired_products = []
    best_before_date = datetime.datetime.today().date() + datetime.timedelta(days=in_advance_days)
    for key, value in items.items():
        quantity = 0
        for product in value:
            if product["expiration_date"] is not None:
                if product["expiration_date"] <= best_before_date:
                    quantity += product["amount"]
        if quantity > 0:
            list_expired_products.append((key, quantity))
    return list_expired_products


# goods = {
#     'Хлеб': [
#         {'amount': Decimal('1'), 'expiration_date': None},
#         {'amount': Decimal('1'), 'expiration_date': datetime.date(2023, 12, 9)}
#     ],
#     'Яйца': [
#         {'amount': Decimal('2'), 'expiration_date': datetime.date(2023, 12, 12)},
#         {'amount': Decimal('3'), 'expiration_date': datetime.date(2023, 12, 11)}
#     ],
#     'Вода': [{'amount': Decimal('100'), 'expiration_date': None}]
# }
# print(expire(goods))
# # Вывод: [('Хлеб', Decimal('1'))]
# print(expire(goods, 1))
# # Вывод: [('Хлеб', Decimal('1')), ('Яйца', Decimal('3'))]
# print(expire(goods, 2))
# # Вывод: [('Хлеб', Decimal('1')), ('Яйца', Decimal('5'))]

add(goods, 'Яйца', Decimal('10'), '2023-9-30')
print(goods)
add(goods, 'Яйца', Decimal('3'), '2023-10-15')
print(goods)
add(goods, 'Вода', Decimal('2.5'))
print(goods)

from datetime import datetime


def make_date(created_at):
    created = created_at.lstrip('< ').split(' ')[2].strip().lower()
    if created == 'ago' or created == 'yesterday':
        created_at = datetime.today().strftime('%d-%m-%Y')
    else:
        list = created_at.split('/')
        created_at = f'{list[0]}-{list[1]}-{list[2]}'
    return created_at


def make_currency(currency):
    if currency.strip()[0] == '$':
        currency = '$'
    else:
        currency = None
    return currency
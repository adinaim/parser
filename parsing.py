import requests
from bs4 import BeautifulSoup, ResultSet
from models import Appartment, db
from utils import make_date, make_currency


def get_html(url: str, headers: dict='', params: str=''):
    html = requests.get(
        url,
        headers=headers,
        params=params,
        verify=False
    )
    print(html.text)
    return html.text


def get_cards_from_html(html: str) -> ResultSet:
    soup = BeautifulSoup(html, 'lxml')
    cards: ResultSet = soup.find_all('div', class_="search-item")
    return cards


def get_card(cards: list) -> list:
    result = []
    for card in cards:
        container = card.find('div', class_='clearfix')
        try:
            image = container.find('img').get('src')
        except:
            image = None
        try:
            created_at = container.find('div', class_='location').find('span', class_='date-posted').text
            created_at = make_date(created_at)
        except:
            created_at = None
        try:
            currency = container.find('div', class_='price').text
            currency = make_currency(currency)
        except:
            currency = None
        apt = {
            'image': image,
            'created_at': created_at,
            'currency': currency
        }
        result.append(apt)
    return result


def parsing() -> list:
    apts = []
    for apt in range(100):
        HOST = f'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-{apt+1}/c37l1700273?ad=offering'
        HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
        html = get_html(HOST, HEADERS)
        cards = get_cards_from_html(html)
        apt = get_card(cards)
        apts.extend(apt)
    print('Ваша БД заполнена!')
    return apts


def parse_into_db():
    db.create_tables([Appartment])
    apts = parsing()
    with db.atomic():
        Appartment.insert_many(apts).execute()
    print('Ваша БД заполнена!')

if __name__ == '__main__':
    parse_into_db()
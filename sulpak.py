from bs4 import BeautifulSoup
import requests
import csv

CSV = 'sulpak_comps.csv'
HOST = 'https://www.sulpak.kg/'
URL = 'https://www.sulpak.kg/f/noutbuki'
HEADERS = {
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'

}

def get_html(url, params = ''):
    r = requests.get(url, headers = HEADERS, params= params, verify=False)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_ = 'goods-tiles')
    news_list = []

    for item in items:
        news_list.append({
            'title' : item.find('h3', class_ = 'title').get_text(strip = True),
            'price' : item.find('div', class_ = 'price-block').get_text(strip = True),
            'nalichi' : HOST + item.find('div', class_ = 'product-container-right-side').find('a').get('href')

        })
    return news_list

def news_save(items, path):
    with open(path, 'a') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Названия', 'Цена', 'Ссылка'])
        for item in items:
            writer.writerow([item['title'], item['price'], item['Ссылка']])

def parser():
    PAGENATION = input("Введите количество страниц: ")
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        news_list = []
        for page in range(1, PAGENATION):
            print(f'Страница №{page} готова')
            html = get_html(URL, params={'page' : page})
            news_list.extend(get_content(html.text))
        news_save(news_list, CSV)
        print('Парсинг готов')
    else:
        print('Error')
parser()
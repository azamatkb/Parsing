from bs4 import BeautifulSoup
import requests
import csv

CSV = 'kivano_automag.csv'
HOST = 'https://www.kivano.kg/'
URL = 'https://www.kivano.kg/avtomagnitoly'
HEADERS = {
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'

}

def get_html(url, params = ''):
    r = requests.get(url, headers = HEADERS, params= params, verify=False)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_ = 'item product_listbox oh')
    news_list = []

    for item in items:
        news_list.append({
            'title' : item.find('h1', class_ = 'stile').get_text(strip = True),
            'price' : item.find('div', class_ = 'product-price2').get_text(strip = True),
            'opisanie' : item.find('div', class_ = 'shop text').get_text(strip = True),
            'nalichie' : item.find('span', class_ = 'status').get_text(strip = True),
            'ssylka' : item.find('div', class_ = 'portlet-title').find('a').get('href')

        })
    return news_list

def news_save(items, path):
    with open(path, 'a') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название: ', ' Цена: ', ' Описание:', ' Наличие:', ' Ссылка: '])
        for item in items:
            writer.writerow([item['title'], item['price'], item['opisanie'], item['nalichie'], item['ssylka']])

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
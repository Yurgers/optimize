"""
Порядок использования:

avito.py -q <query> -c <category>

параметры:
-q     --query       что ищем
-c     --category    в каких категории, путь можно перечислить через пробел или /

"""

import argparse
import csv
import re
import sys

import requests
from bs4 import BeautifulSoup

#https://www.avito.ru/moskva/telefony/xiaomi?q=xiaomi&p=3
#base_url= 'https://www.avito.ru/moskva/telefony?p={0}&q={1}'
base_url= 'https://www.avito.ru/moskva'
avito_query = 'xiaomi'
category = []
pages = 1
symma = 0


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-q', '--query')
    parser.add_argument ('-c', '--category', default='telefony/xiaomi' )    #telefony

    return parser


def get_html(url, query, page):
    #print(url, query, page)
    r = requests.get(url, {'q':query, 'p':page})
    #r = requests.get('https://www.avito.ru/moskva?q=xiaomi&p=1')
    #print(r.url)
    if '/blocked' in r.url:
        print("Нас заблокировали!")
        print(r.text)
        exit()
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='pagination-pages').find_all('a')[-1].get('href')
    pages = re.findall(r'p=(\d+)&', pages)[0]
    return int(pages)


def write_csv(data):
    with open('avito.csv', 'a', newline='') as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerow((data['title'],
                          data['price'],
                          data['date'],
                          data['metro'],
                          data['url']))

        f.close()


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    #print (soup)
    #catalog-list clearfix      js-catalog_after-ads
    ads = soup.find('div', class_='js-catalog_after-ads').find_all('div', class_='item_table-description')
    global symma
    symma += len(ads)
    #print(ads)
    for ad in ads:
        #title, url, price, metro, data
        title = ad.find('a', class_='item-description-title-link').text.strip()
        #print(title)

        url = ad.find('a', class_='item-description-title-link').get('href')
        url = 'https://www.avito.ru' + url
        #print(url)

        price = ad.find('div', class_='about').text.strip()
        #print(price)

        date = ad.find('div', class_='date').text.strip()
        #print(date)

        datas = ad.find_all('p')
        if datas:
            for data in datas:
                #print
                if 'м.' in data.text:
                    metro = data.text.strip()
            #print(metro)

        else:
            metro = ''


        data = {
                'title':title,
                'url':url,
                'price':price,
                'date':date,
                'metro':metro
                }
        #print(data)
        write_csv(data)

if __name__ == '__main__':
    #url = base_url.format(1, avito_query)
    f = open('avito.csv', 'w')
    f.close()

    #avito_query
    arguments = createParser().parse_args(sys.argv[1:])
    #print(namespace)

    if not arguments.query:
        print(__doc__)
        exit()

    avito_query = arguments.query
    category.extend(arguments.category.split())

    if not category:
        category = ['']

    if category != ['']:
        base_url = base_url + '/'

    url = base_url + '/'.join(category)
    #print(url)

    pages = get_total_pages(get_html(url, avito_query, pages))
    #print(pages)
    #for p in range(1, pages+1):
    for p in range(1, 3):
        html = get_html(url, avito_query, p)
        get_page_data(html)
    category = '/'.join(category)
    print('найдено %s товаров %s в категории %s' % (symma, avito_query, category) )





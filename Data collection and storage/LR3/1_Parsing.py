import requests
from bs4 import BeautifulSoup
from lxml import html

import csv
import fake_useragent

user = fake_useragent.UserAgent().random
headers = {
    'user-agent': user,
    # Я хочу получить HTML-страницу (text/html) или XML (application/xml), но если ничего не подходит, дай мне что угодно
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

link = 'https://opencritic.com/browse/all?page=1'
#Получение HTML
response = requests.get(link, headers=headers).text

def beautiful_soup():
    #soup - объект
    soup = BeautifulSoup(response, 'lxml')
    #items - общий контейнер
    items = soup.find_all('div', class_='row no-gutters py-2 game-row align-items-center')
    games_data = []
    for item in items[:10]:
        score_elem = item.find('div', class_='inner-orb small-orb')
        name_elem = item.find('div', class_='game-name col ml-2')
        platforms_elem = item.find('div', class_='platforms col-auto')
        genres_elem = item.find('div', class_='genres mx-4')
        date_elem = item.find('div', class_='first-release-date col-auto show-year')

        score = score_elem.get_text(strip=True) if score_elem else "N/A"
        name = name_elem.get_text(strip=True) if name_elem else "N/A"
        platforms = platforms_elem.get_text(strip=True) if platforms_elem else "N/A"
        genres = genres_elem.get_text(strip=True) if genres_elem else "N/A"
        release_date = date_elem.get_text(strip=True) if date_elem else "N/A"
        
        games_data.append({
            'Название': name,
            'Рейтинг': score,
            'Жанры': genres,
            'Дата выхода': release_date,
            'Платформы': platforms
        })
    return games_data
def lxml():
    # упорядычивает текст в дерево, ветки
    tree = html.fromstring(response)
    
    # Найди в любом месте (//) страницы все теги <div>, у которых одновременно
    #В атрибуте class содержится слово game-row и row
    items = tree.xpath('//div[contains(@class, "game-row") and contains(@class, "row")]')

    games_data = []
    for item in items[:10]:
        #/text() - извлекает число из найденной строчки <div class="inner-orb small-orb">95</div>
        score_elements = item.xpath('.//div[contains(@class, "inner-orb") and contains(@class, "small-orb")]/text()')
        score = score_elements[0].strip() if score_elements else "N/A"
        
        # Найди div с нужным классом, затем зайди внутрь него, найди тег <a> - Заголовок
        name_elements = item.xpath('.//div[@class="game-name col ml-2"]/a/text()')
        name = name_elements[0].strip() if name_elements else "N/A"
        
        platforms_elements = item.xpath('.//div[contains(@class, "platforms") and contains(@class, "col-auto")]')
        platforms = platforms_elements[0].text_content().strip() if platforms_elements else "N/A"
        
        genres_elements = item.xpath('.//div[contains(@class, "genres") and contains(@class, "mx-4")]')
        genres = genres_elements[0].text_content().strip() if genres_elements else "N/A"
        
        date_elements = item.xpath('.//div[contains(@class, "first-release-date") and contains(@class, "col-auto") and contains(@class, "show-year")]/span/text()')
        release_date = date_elements[0].strip() if date_elements else "N/A"
        
        games_data.append({
            'Название': name,
            'Рейтинг': score,
            'Жанры': genres,
            'Дата выхода': release_date,
            'Платформы': platforms
        })
    return games_data
def write_csv(parsing):
    with open('games_bs.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Название', 'Рейтинг', 'Жанры', 'Дата выхода', 'Платформы']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames) 
        #(fieldnames=fieldnames) - делает структру словоря, привязывая Переменные GAME_DATA в порядке указанном fieldnames.
        # Важно что бы Названия совпадали.

        #Запись
        writer.writeheader()  # Записываем заголовки столбцов в 1-0й строчке (вещь опциональная)
        for row in parsing:
            writer.writerow(row)  # Записываем каждую строку

write_csv(beautiful_soup())
#write_csv(lxml())


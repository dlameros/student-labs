import requests
import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

#ключ зажигания
service = Service()
# Настройка трактора залезаем под капот и настраиваем
chrome_options = webdriver.ChromeOptions()
#Скрытный трактор ('--headless') - Пусть никто не видит как ты пашешь,
#Не проверяй каждый сотку (--no-sandbox) - работай по всему полю
#Не используй общую память (--disable-dev-shm-usage) 
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


# Возьми ключ (service) и настройки(сhrome_option), собери мне мега комбайн.
wd = webdriver.Chrome(service=service,options=chrome_options)

# Комбайн умеет переходить по ссылке(get), ждать(implicitly_wait), кликать кнопки(execute_script), показывать что видит(page_source)
wd.get("https://www.news29.ru/novosti/ekonomika/")
wd.implicitly_wait(10)
print(wd.title) # Трактор знает на каком поле пашет.
#Выводы
#Service() — это ключ.
#ChromeOptions() — это инструкция по настройке.
#webdriver.Chrome(...) — это сам заведённый трактор. 
#Ты не едешь на ключе. Ты не пашешь по инструкции. Ты пашешь трактором.

# Parse - алгоритм сортирующий все что собрал трактор, аналогичный алгоритм из первого задания
def parse():
    #wd.page_source - передаем html мусор собранный трактором
    soup = BeautifulSoup(wd.page_source, features="lxml") 
    location_blocks = soup.find_all('div', {'class': 'newItemContainer'}) 
    data = []
    for block in location_blocks:

        # Заголовок
        title_div = block.find('div', {'class': 'title'})
        title_tag = title_div.find('a') if title_div else None 
        title = title_tag.text.strip() if title_tag else "Без заголовка"

        # Ссылка
        link = title_tag.get('href') if title_tag else "Ссылка отсутствует"

        #Текст
        lead_div = block.find('div', {'class': 'lead'})
        text = lead_div.text.strip() if lead_div else "Текст отсутствует"
        
        # Дата
        viewscount = block.find('div', {'class': 'viewscount'})
        
        date_tag  = viewscount.find('div', {'class': 'date'})
        date = date_tag.text.strip() if date_tag else "Дата отсутствует"
        
        # Просмотры
        eye_icon = viewscount.find('img', {'class', 'icon'})
        view_text = eye_icon.next_sibling if eye_icon else None
        views = view_text.strip() if view_text and isinstance(view_text, str) else "0"

        data.append({
            'Название': title,
            'Текст': text,
            'Дата': date,
            'Просмотры': views,
            'Ссылка': link
        })
    return data
def write_csv(parsing):
    with open('harvest_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Название', 'Текст', 'Дата', 'Просмотры', 'Ссылка']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames) 

        writer.writeheader()
        for row in parsing:
            writer.writerow(row)

# WebDriverWait(wd, 30) — это умный помощник, который следит за трактором и ждёт, когда появится кнопка.
# Без трактора (wd) помощник не знает, за чем следить. 
wait = WebDriverWait(wd, 30)
#until - как только кнопка появится можно нажимать
wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'newsListContainer')))

x = 0
max_clicks = 5  # Максимум попыток
while x < max_clicks:
    time.sleep(0.5)
    # Проверяем, существует ли кнопка #moreNews и видна ли она
    try:
        more_button = wd.find_element(By.CSS_SELECTOR, "#moreNews")
        if more_button.is_displayed() and more_button.is_enabled():
            wd.execute_script("arguments[0].click();", more_button)
        else:
            print("Кнопка 'Показать ещё' неактивна или скрыта. Прекращаем.")
            break
    except Exception as e:
        print("Новости, вероятно, закончились.")
        break
    x += 1

time.sleep(2)
write_csv(parse())

time.sleep(2)
# Вызов алгоритма для сортировки всего что собрали
write_csv (parse())
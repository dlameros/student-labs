import requests
import fake_useragent
from bs4 import BeautifulSoup

user = fake_useragent.UserAgent().random
header =  {'user-agent': user}

link = "http://browser-info.ru/"
".content - передает информацию в байтах"
"requests.get(link) - запрос к сайту с целью получить информацию"
responce = requests.get(link, headers=header).text
"BuautifulSoup - принимает в качестве значений теги HTML"
soup = BeautifulSoup(responce, 'lxml')
"find - ищет 1 совпадение, find_all - ищет все совпадения для div"
block = soup.find('div', id = "tool_padding")

#check_js
check_js = block.find('div', id = 'javascript_check')
#Помещаем значкение включен ли жава скрипт или выключен, в Check_js есть 2 тега Spam, 
# поэтому мы ищем через тег Find_all. и 1 значение выведем как текст
status_js = check_js.find_all('span')[1].text
result_js = f'javascript: {status_js}'

#check_flash
check_flash = block.find('div', id = 'flash_version')
status_flash = check_flash.find_all('span')[1].text
result_flash = f'flash: {status_flash}'

#user_agent
check_user = block.find('div', id='user_agent').text
print(result_js, result_flash, check_user)

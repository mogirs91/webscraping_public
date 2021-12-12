import requests
import re
from bs4 import BeautifulSoup
from time import sleep
from random import uniform
import pandas as pd

df_data = pd.DataFrame()
urla = 'http://www.finmarket.ru/'
user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'

session = requests.Session()
session.headers.update({'User-Agent':user_agent_val})
searchdirectory ='http://www.finmarket.ru/database/organization/search.asp?l='

for cros in range(54):
    requestlink = BeautifulSoup(session.get(f'{searchdirectory}{cros}').text, 'html.parser')
    # поиск ссылок по всем ссылкам для данной страницы
    itemlinks = requestlink.find_all('a', class_='fs13 black')
    # обход данных в таблице для каждой страницы
    for itemlink in itemlinks:
        sleep(uniform(3,6))
        clearlink = 'http://www.finmarket.ru' + itemlink.get('href')
        pageenc = session.get(clearlink)
        pageenc.encoding = 'cp1251'
        souplink = BeautifulSoup(pageenc.text, 'html.parser')
        pageelems = souplink.find(class_='cmn_info')
        try:
            name = pageelems.find('td', text=re.compile('Наименование:')).next_sibling.get_text()
        except:
            name = 'не_найдено'
        try:
            okved = pageelems.find('td', text=re.compile('Основной ОКВЭД:')).next_sibling.get_text()
        except:
            okved = 'не_найдено'
        try:
            country = pageelems.find('td', text=re.compile('Страна:')).next_sibling.get_text()
        except:
            country = 'не_найдено'
        try:
            region = pageelems.find('td', text=re.compile('Регион:')).next_sibling.get_text()
        except:
            region = 'не_найдено'
        try:
            inn = pageelems.find('td', text=re.compile('ИНН:')).next_sibling.get_text()
        except:
            inn = 'не_найдено'
        try:
            okpo = pageelems.find('td', text=re.compile('ОКПО или др.:')).next_sibling.get_text()
        except:
            okpo = 'не_найдено'
        try:
            uradr = pageelems.find('td', text=re.compile('Юридический адрес:')).next_sibling.get_text()
        except:
            uradr = 'не_найдено'
        try:
            site = pageelems.find('td', text=re.compile('Web сайт:')).next_sibling.get_text()
        except:
            site = 'не_найдено'
        try:
            tel = str(pageelems.find('td', text=re.compile('Контакты:')).next_sibling.get_text()).split('E')[0]
        except:
            tel = 'не_найдено'
        try:
            email = str(pageelems.find('td', text=re.compile('Контакты:')).next_sibling.get_text()).split('E-')[1]
        except:
            email = 'не_найдено'
        print(name,okved,country,region,inn,okpo,uradr,site,tel,email)
        df_data = df_data.append({'Наименование': name, 'Основной ОКВЭД': okved, 'Страна': country, 'Регион': region, 'ИНН': inn, 'ОКПО': okpo, 'Юридический адрес': uradr, 'Сайт': site, 'Телефон': tel, 'Email': email}, ignore_index=True)
        df_data = df_data.reindex(columns=['Наименование','Основной ОКВЭД','Страна','Регион','ИНН','ОКПО','Юридический адрес','Сайт','Телефон','Email'])

print(df_data)
#df_data.to_excel(r'C:\Users\Admin\Desktop\Обучение Питон\Питон парсинг\Финмаркет\result.xlsx',index=False)
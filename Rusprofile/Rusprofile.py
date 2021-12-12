import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import pickle
from random import uniform

url = 'https://www.rusprofile.ru'
user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.'

#логины и пароли
login = 'ltdan@yandex.ru'

#сессия для входа с паролем - для поиска контактов
session = requests.Session()
session.headers.update({'Referer':url})
session.headers.update({'User-Agent':user_agent_val})
searchdirectory = 'https://www.rusprofile.ru/search?query='

# открыть куки из пикл файла
cookies = pickle.load(open(login,'rb'))

for cookie in cookies:
    if 'httpOnly' in cookie:
        httpO = cookie.pop('httpOnly')
        cookie['rest'] = {'httpOnly': httpO}
    if 'expiry' in cookie:
        cookie['expires'] = cookie.pop('expiry')
    if 'sameSite' in cookie:
        cookie.pop('sameSite')
    session.cookies.set(**cookie)

#создание объектов Pandas
df_inns = pd.DataFrame()
df_results = pd.DataFrame()
df_inns = pd.read_excel(r'C:\Users\Admin\Desktop\Обучение Питон\Питон парсинг\Руспрофайл\input.xlsx', index_col=None, header=None)
inns = df_inns[0].tolist()
print(inns)

counter = 0
for inn in inns:
    sleep(uniform(15,19))
    counter = counter + 1
    print(f'обрабатывается ИНН №{counter}', f'{searchdirectory}{inn}')
    try:
        souplink = BeautifulSoup(session.get(f'{searchdirectory}{inn}').text, 'html.parser')
        name = souplink.find('div', class_='company-name').get_text()
        rawtels = souplink.find_all('a', itemprop='telephone')
        rawmails = souplink.find_all('a', itemprop='email')
        tellist = []
        maillist = []
        for rawtel in rawtels:
            tellist.append(rawtel.get_text())
        for rawmail in rawmails:
            maillist.append(rawmail.get_text())
        print(inn,name,tellist,maillist)
        df_results = df_results.append({'ИНН': inn, 'Название': name, 'Список телефонов': tellist, 'Список эл. почты': maillist}, ignore_index=True)
    except:
        print('пройти по ссылке не удалось или что-то пошло не так')

try:
    df_results.to_excel(r'C:\Users\Admin\Desktop\Обучение Питон\Питон парсинг\Руспрофайл\result.xlsx',index=False)
except:
    print('нет результатов для записи в файл или что-то пошло не так')
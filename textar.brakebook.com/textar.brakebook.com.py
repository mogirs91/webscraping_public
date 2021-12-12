import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import pandas as pd
import pickle
from random import uniform
import re
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

#about config - проверка настроек Firefox, фоновый режим
option = webdriver.FirefoxOptions()
option.set_preference('dom.webdriver.enabled', False)
option.set_preference('dom.webnotifications.enabled', False)
option.set_preference('dom.media.volume_scale', '0.0')
option.set_preference('general.useragent.override', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.')
option.headless = True
browser = webdriver.Firefox(options=option)

#создание объектов Pandas
df_numbers = pd.DataFrame()
df_models = pd.DataFrame()
df_volumes = pd.DataFrame()
df_attributes = pd.DataFrame()
df_powers = pd.DataFrame()
df_years = pd.DataFrame()
df_results = pd.DataFrame()

df_numbers = pd.read_excel(r'C:\Users\Admin\Desktop\Обучение Питон\Питон парсинг\Textar\input.xlsx', index_col=None, header=None)
numbers = df_numbers[0].tolist()

def parser(number):
    global df_numbers
    global df_models
    global df_volumes
    global df_attributes
    global df_powers
    global df_years
    global df_subresults
    global df_results
    global markavalue
    global volumevalue
    global modelvalue
    global markacounter
    global modelcounter1
    global modelcounter3
    global modelcounter4
    global counter

    searchdirectory = 'https://textar.brakebook.com/bb/textar/ru_RU/PKW/applicationSearch.xhtml'
    sleep(uniform(3,5))
    print(f'обрабатывается номер №{number}')
    browser.get(f'{searchdirectory}')
    try:
        browser.find_element_by_class_name('acceptButton').click()
    except:
        pass
    number_input = browser.find_element_by_id('search_keywords')
    number_input.clear()
    number_input.send_keys(f'{number}')
    sleep(uniform(2, 4))
    number_input.send_keys(Keys.ENTER)
    sleep(uniform(7, 10))

    rawlinks = browser.find_elements_by_class_name('datasheetLink')
    rawlinklist = []
    linklist = []
    for rawlink in rawlinks:
        sleep(uniform(5, 7))
        link = rawlink.get_attribute('href')
        rawlinklist.append(link)
    linklist = list(set(rawlinklist))

    #обход всех ссылок с товарами
    for i in linklist:
        browser.get(i)
        sleep(uniform(3, 4))
        #обход всех элементов с выпадающими таблицами и подробностями
        openelems = browser.find_elements_by_xpath("//td[@class='name']")
        for openelem in openelems:
            sleep(uniform(3, 4))
            openelem.click()

        marks = list(browser.find_elements_by_class_name('block'))

        markacounter = 2
        for mark in range(len(marks)):
            models = browser.find_elements_by_xpath(f"//form/div[{markacounter}]//div[@class='model']//table[@class='model']")
            markavalue = browser.find_element_by_xpath(f"//form/div[{markacounter}]/div")

            modelcounter1 = 1
            modelcounter2 = 1
            modelcounter3 = 1
            modelcounter4 = 1

            for model in models:
                print(model.text)
                volumes = browser.find_elements_by_xpath(f"//form/div[{markacounter}]//div//div//div[{modelcounter1}]//table[2]/tbody/tr[2]/td[2]/div/div/div/table/tbody//td[1]/a")
                for volume in volumes:
                    df_volumes = df_volumes.append({'Поисковый_номер': number, 'Ссылка': i, 'Марка': markavalue.text, 'Модель': model.text,'Объем_двигателя': volume.text}, ignore_index=True)
                    df_volumes = df_volumes.reindex(columns=['Поисковый_номер', 'Ссылка', 'Марка','Модель','Объем_двигателя'])
                modelcounter1 = modelcounter1 + 1

            for model in models:
                years = browser.find_elements_by_xpath(f"//form/div[{markacounter}]//div//div//div[{modelcounter2}]//table[2]/tbody/tr[2]/td[2]/div/div/div/table/tbody//td[2]")
                for year in years:
                    pattern = re.compile(r'/')
                    match = re.search(pattern, str(year.text))
                    if match:
                        df_years = df_years.append({'Года_выпуска': year.text}, ignore_index=True)
                    else:
                        pass
                modelcounter2 = modelcounter2 + 1

            for model in models:
                powers = browser.find_elements_by_xpath(f"//form/div[{markacounter}]//div//div//div[{modelcounter3}]//table[2]/tbody/tr[2]/td[2]/div/div/div/table/tbody//td[3]")
                for power in powers:
                    df_powers = df_powers.append({'Квт': power.text}, ignore_index=True)
                modelcounter3 = modelcounter3 + 1

            for model in models:
                attributes = browser.find_elements_by_xpath(f"//form/div[{markacounter}]//div//div//div[{modelcounter4}]//table[2]/tbody/tr[2]/td[2]/div/div/div/table/tbody/tr[1]/td[4]")
                attributelist = []
                for attribute in attributes:
                    attributelist.append(str(attribute.text).strip().replace('\n','/'))
                df_attributes = df_attributes.append({'Поисковый_номер': number, 'Ссылка': i,  'Марка': markavalue.text,'Модель': model.text,'Доп_инфо': attributelist}, ignore_index=True)
                df_attributes = df_attributes.reindex(columns=['Поисковый_номер','Ссылка','Марка','Модель','Доп_инфо'])
                modelcounter4 = modelcounter4 + 1
            markacounter = markacounter + 1
            print('конец марки')

    return(linklist)

for n in range(len(numbers)):
    print('первая попытка')
    res = parser(numbers[n])
    if res == []:
        print('вторая попытка')
        parser(numbers[n])
    else:
        n + 1

# огромный try блок вместо def
# повысить быстродействие
# протестировать на множестве артикулов

df_subresults = pd.concat([df_volumes, df_years, df_powers], axis=1).dropna()
df_results = pd.merge(df_subresults, df_attributes, on=['Поисковый_номер','Ссылка','Марка','Модель'], how='left').dropna()

#df_volumes.to_excel(r'C:\Users\Admin\Desktop\Обучение Питон\Питон парсинг\Textar\volumes.xlsx',index=False)
#df_years.to_excel(r'C:\Users\Admin\Desktop\Обучение Питон\Питон парсинг\Textar\years.xlsx',index=False)
#df_powers.to_excel(r'C:\Users\Admin\Desktop\Обучение Питон\Питон парсинг\Textar\powers.xlsx',index=False)
#df_attributes.to_excel(r'C:\Users\Admin\Desktop\Обучение Питон\Питон парсинг\Textar\attributes.xlsx',index=False)
#df_subresults.to_excel(r'C:\Users\Admin\Desktop\Обучение Питон\Питон парсинг\Textar\subresult.xlsx',index=False)

df_results = df_results.reindex(columns=['Поисковый_номер','Ссылка','Марка','Модель','Объем_двигателя','Года_выпуска', 'Квт', 'Доп_инфо'])
df_results.to_excel(r'C:\Users\Admin\Desktop\Обучение Питон\Питон парсинг\Textar\result.xlsx',index=False)

browser.quit()


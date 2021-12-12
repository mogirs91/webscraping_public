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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#настройки Chrome, фоновый режим
option = webdriver.ChromeOptions()
option.add_experimental_option("excludeSwitches", ["enable-automation"])
#option.add_argument("--headless")
option.add_argument("--disable-gpu")
option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36")
browser = webdriver.Chrome(options=option)

#входной файл
df_numbers = pd.read_excel(r'C:\Users\Admin\Desktop\Обучение Питон\Питон парсинг\Dayco\input.xlsx', index_col=None, header=None)
numbers = df_numbers[0].tolist()

#создание объектов Pandas
df_numbers = pd.DataFrame()
df_results = pd.DataFrame()

counter = 0
global lenmarkas
global lenmodels
global i
global j

def go_to_tovar(number):
    browser.set_window_size(1920,1080)
    browser.get('https://www.daycogarage.com/catalogue/ru-ru/search-product-by-code?a=1')
    sleep(uniform(3, 5))
    browser.find_element_by_id("Tipologia").click()
    sleep(uniform(3, 5))
    browser.find_element_by_xpath('/html/body/form/div[7]/div/div/span/div/div[2]/div[1]/ul/li[2]/div/span').click()
    search_input = browser.find_element_by_id('inputCode')
    search_input.clear()
    search_input.send_keys(number)
    sleep(uniform(1, 2))
    search_input.send_keys(Keys.ENTER)
    sleep(uniform(6, 8))

for number in numbers:
    counter = counter + 1
    print(f'обрабатывается №{counter}', f'{number}')
    go_to_tovar(number)
    try:
        markas = browser.find_elements_by_xpath('//ul[@id="ListaMarca"]/li')
        sleep(uniform(5, 7))
        lenmarkas = len(markas)
    except:
        lenmarkas = 1

    for i in range(lenmarkas):
        go_to_tovar(number)
        if lenmarkas != 1:
            marka = browser.find_element_by_xpath(f'//ul[@id="ListaMarca"]/li[{i + 1}]')
            #/html/body/form/div[7]/div/div/span/div/div[2]/div[3]/ul/li[10]/div/span
            print(i,'номер текущей марки')
            marka.click()
            fmodel = marka.text
        else:
            marka = browser.find_element_by_xpath(f'//div[@id="Marca"]/span')
            fmarka = marka.text
        print(marka.text)
        sleep(uniform(5, 7))
        models = browser.find_elements_by_xpath('//ul[@id="ListaGamma"]/li')
        lenmodels = len(models)
        print(lenmodels,'кол-во моделей')

        for j in range(lenmodels):
            go_to_tovar(number)
            if lenmarkas != 1:
                try:
                    marka = browser.find_element_by_xpath(f'//ul[@id="ListaMarca"]/li[{i + 1}]')
                #/html/body/form/div[7]/div/div/span/div/div[2]/div[3]/ul/li[4]/div/span
                #ошибка в строке ниже #6PK1735 и в строке выше #6PK1530
                    marka.click()
                    fmarka = marka.text
                except:
                    go_to_tovar(number)
                    sleep(uniform(3,5))
                    marka = browser.find_element_by_xpath(f'//ul[@id="ListaMarca"]/li[{i + 1}]')
                    # /html/body/form/div[7]/div/div/span/div/div[2]/div[3]/ul/li[4]/div/span
                    # ошибка в строке ниже #6PK1735 и в строке выше #6PK1530
                    marka.click()
                    fmarka = marka.text
            else:
                marka = browser.find_element_by_xpath(f'//div[@id="Marca"]/span')
                fmarka = marka.text
            sleep(uniform(4, 5))
            if lenmodels != 1:
                model = browser.find_element_by_xpath(f'//ul[@id="ListaGamma"]/li[{j + 1}]')
                model.click()
                fmodel = model.text
            else:
                model = browser.find_element_by_xpath(f'//div[@id="Gamma"]/span')
                fmodel = model.text
            sleep(uniform(4, 5))
            application = browser.find_element_by_xpath(f'//li[@id="applications"]/a')
            application.click()
            apptable = browser.find_element_by_xpath(f'//div[@id="applicationTable"]/table/tbody')
            oems = str(apptable.text).split('\n')
            dmodels = browser.find_elements_by_xpath(f'//span[@title="Модель"]')
            dmodelcounter = 0
            for m in range(len(dmodels)):
                dmodel = browser.find_element_by_xpath(f'/html/body/form/div[7]/div/div/span/div/div[3]/div[3]/div[5]/div/div[{dmodelcounter+2}]/table[1]/thead/tr/th[2]/span[1]').text
                volume = browser.find_element_by_xpath(f'/html/body/form/div[7]/div/div/span/div/div[3]/div[3]/div[5]/div/div[{dmodelcounter+2}]/table[1]/thead/tr/th[2]/span[3]').text
                generation = browser.find_element_by_xpath(f'/html/body/form/div[7]/div/div/span/div/div[3]/div[3]/div[5]/div/div[{dmodelcounter+2}]/table[1]/thead/tr/th[4]/span').text
                engine = browser.find_element_by_xpath(f'/html/body/form/div[7]/div/div/span/div/div[3]/div[3]/div[5]/div/div[{dmodelcounter+2}]/table[2]/tbody/tr/td[2]//span').text
                cc = browser.find_element_by_xpath(f'/html/body/form/div[7]/div/div/span/div/div[3]/div[3]/div[5]/div/div[{dmodelcounter+2}]/table[2]/tbody/tr/td[3]').text
                horsepower = browser.find_element_by_xpath(f'/html/body/form/div[7]/div/div/span/div/div[3]/div[3]/div[5]/div/div[{dmodelcounter+2}]/table[2]/tbody/tr/td[4]').text
                year = browser.find_element_by_xpath(f'/html/body/form/div[7]/div/div/span/div/div[3]/div[3]/div[5]/div/div[{dmodelcounter+2}]/table[2]/tbody/tr/td[5]').text
                tecdoc = browser.find_element_by_xpath(f'/html/body/form/div[7]/div/div/span/div/div[3]/div[3]/div[5]/div/div[{dmodelcounter+2}]/table[2]/tbody/tr/td[6]').text
                dmodelcounter = dmodelcounter + 2
                df_results = df_results.append({'Поисковый_номер': number, 'Оригиналы': oems, 'Марка': fmarka, 'Модель': fmodel, 'Модель_подробно':dmodel,'Двигатель': engine, 'Поколение': generation, 'Год': year, 'Рабочий объем' : volume, 'Мощность в л.с.': horsepower, 'сс' : cc, 'Текдок' : tecdoc}, ignore_index=True)
                df_results = df_results.reindex(columns=['Поисковый_номер','Оригиналы','Марка','Модель','Модель_подробно','Двигатель','Поколение','Год','Рабочий объем','Мощность в л.с.','сс','Текдок'])

df_results.to_excel(r'C:\Users\Admin\Desktop\Обучение Питон\Питон парсинг\Dayco\result.xlsx',index=False)
browser.quit()


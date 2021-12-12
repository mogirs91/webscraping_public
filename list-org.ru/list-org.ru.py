import requests
import re
from bs4 import BeautifulSoup
from time import sleep
from random import uniform
import pandas as pd
from selenium import webdriver
import ssl
#ssl._create_default_https_context = ssl._create_unverified_context

#df_data = pd.DataFrame()

usepr = '87.237.234.187:3128'
#about config - проверка настроек Firefox, фоновый режим
options = webdriver.FirefoxOptions()
options.set_preference('dom.webdriver.enabled', False)
options.set_preference('dom.webnotifications.enabled', False)
options.set_preference('dom.media.volume_scale', '0.0')
options.set_preference('general.useragent.override', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0')
options.headless = False
caps = webdriver.DesiredCapabilities.FIREFOX
#caps['marionette'] = True
caps['pageLoadStrategy'] = 'eager'
caps['proxy'] = {
    "proxyType": "MANUAL",
    "httpProxy": usepr,
    "ftpProxy": usepr,
    "sslProxy": usepr
}
browser = webdriver.Firefox(options=options,capabilities=caps)

url = 'https://22.list-org.ru/'
user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'
proxies = {'http': f'{usepr}','https':f'{usepr}'}

session = requests.Session()
session.headers.update({'User-Agent':user_agent_val})
session.headers.update({'Referer':url})
#session.proxies.update(proxies)
searchdirectory ='https://22.list-org.ru/razdel-transport_gruzoperevozki-'
#print(f'{searchdirectory}1.html')

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

#'//22.list-org.ru/59566-aa_pervaya_kliningovaya_kompaniya_ooo.htm',
clearlinks = ['//22.list-org.ru/59548-aasm_sibir_ooo.htm']
#counter = 0
# for cros in range(1,2):
#     #urllib.request.urlopen(f'{searchdirectory}{cros}.html')
#     requestlink = BeautifulSoup(session.get(f'{searchdirectory}{cros}.html',proxies=proxies,verify=False).text, 'html.parser')
#     # поиск ссылок по всем ссылкам для данной страницы
#     itemlinks = requestlink.find_all('a', class_='m0')
#     # обход данных в таблице для каждой страницы
#     for itemlink in itemlinks:
#         #sleep(uniform(3,6))
#         clearlink = itemlink.get('href')
#         clearlinks.append(clearlink)
# print(clearlinks)

# ООО "ААСМ-СИБИРЬ" - название в поиске ИНН

for clearlink in clearlinks:
    #try:
    browser.get('https:'+clearlink+'l')
    #скопировать имя компании
    sleep(uniform(10, 15))
    name = browser.find_element_by_xpath("//strong[@class='fn org']").text
    print(name)

    # скопировать телефон компании
    browser.find_element_by_id('zphon').click()
    sleep(uniform(10, 15))
    browser.find_element_by_id('zphon').click()
    tel = browser.find_element_by_xpath("//a[@class='blink tel']").text

    # скопировать эл.почту компании
    browser.find_element_by_id('zmail').click()
    sleep(uniform(10, 15))
    browser.find_element_by_id('zmail').click()
    email = browser.find_element_by_xpath("//a[@class='blink email']").text
    print(name,tel,email)
    # except:
    #     print(clearlink)
    #     print('нет контактов')


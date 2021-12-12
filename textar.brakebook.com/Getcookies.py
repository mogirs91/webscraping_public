import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import openpyxl
from random import uniform
import pickle
import pandas as pd

#about config - проверка настроек Firefox
option = webdriver.FirefoxOptions()
option.set_preference('dom.webdriver.enabled', False)
option.set_preference('dom.webnotifications.enabled', False)
option.set_preference('dom.media.volume_scale', '0.0')
option.set_preference('general.useragent.override', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.')
#фоновый режим
option.headless = False

browser = webdriver.Firefox(options=option)

#сохранение логина и пароля
browser.get('https://textar.brakebook.com/bb/textar/ru_RU/PKW/applicationSearch.xhtml')
sleep(30)
pickle.dump(browser.get_cookies(), open('textarcookies','wb'))
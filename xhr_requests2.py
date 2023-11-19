import json
import os
import ast
import time
import pathlib

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from datetime import date, timedelta, datetime
from time import time
from time import sleep
from time import strftime
from time import localtime
####### END OF IMPORTS #########


with open('asdfasdfasdf.txt', 'r', encoding='utf-8') as file:
    requests_file = file.read()


# print(requests_file)

soup = BeautifulSoup(requests_file, 'html.parser')
# print(soup)
print(type(soup))

# script_div = soup.find('script', {'id' : '__NEXT_DATA_'})
script_div = soup.find('script', type='application/json')
script_div = json.loads(script_div.string)

# print(script_div)
print(type(script_div))
print(script_div.keys())
print(script_div['props']['pageProps']['data']['summoner_id'])


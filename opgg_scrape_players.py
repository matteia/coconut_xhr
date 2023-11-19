### using opgg_one_player_fx

import os
import ast
import pathlib

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

from opgg_one_player_fx import scrape_one_player

###################### END OF IMPORTS


script_directory = pathlib.Path().absolute()

options = Options()
options.add_argument(f"user-data-dir={script_directory}/sele_profiles/selenium_prof")
options.add_argument('--disable-application-cache')
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option("detach", True)
# options.add_argument("--headless=new")

# Set up any necessary configurations or options
driver = webdriver.Chrome(options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """})



filename = '../soloq_scrape/scraped_results/partitions_200plus/bronze/partition_0.txt'


with open(filename, 'rb') as f:
    one_list = f.read()

one_list = one_list.decode('utf-8')
one_list = ast.literal_eval(one_list)

#### timer ##############################
start = time()
print(strftime('%Y-%m-%d %H:%M:%S', localtime()))
print('\n')
##############################

players = ['으끄으끄', '이즈이즈', 'ㅁㄹㅇㅎㅁㅇㅀ']
# players = ['으끄으끄', 'ㅁㄹㅇㅎㅁㅇㅀ', '이즈이즈']
# players = ['ㅁㄹㅇㅎㅁㅇㅀ']

for player in players:
    result = scrape_one_player(driver, player)

    print(result)
    print(len(result))


##############################
print("done in %0.3fs." % (time() - start))
print(strftime('%Y-%m-%d %H:%M:%S', localtime()))


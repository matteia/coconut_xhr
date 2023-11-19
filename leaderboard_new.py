import os
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

from time import time
from time import sleep
from time import strftime
from time import localtime
# from tqdm import tqdm

from leaderboard_fx import scrape_leaderboard

from datetime import date, timedelta, datetime
####### END OF IMPORTS #########

start = time()
print(strftime('%Y-%m-%d %H:%M:%S', localtime()))
print('\n')


start_page_number = 23982

number_of_pages = 18
end_page_number = start_page_number + number_of_pages

# end_page_number = 24000
# number_of_pages = end_page_number - start_page_number

print(end_page_number)

result = scrape_leaderboard(start_page_number, number_of_pages, 'ysghs')

print(result)







print("done in %0.3fs." % (time() - start))
print(strftime('%Y-%m-%d %H:%M:%S', localtime()))
sleep(100000)

### Gold 1 99 : p 10466 10468
### Silver 1 99 : p 16787
### Bronze 1 99 : p 22913 22979




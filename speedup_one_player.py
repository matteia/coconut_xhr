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

from datetime import date, timedelta, datetime
from time import time
from time import sleep
from time import strftime
from time import localtime
####### END OF IMPORTS #########


start = time()
print(strftime('%Y-%m-%d %H:%M:%S', localtime()))
print('\n')
#####################################

# target_url = 'https://www.daum.net'
# target_url = 'https://www.op.gg'
target_url = 'https://www.op.gg/leaderboards/tier?page=22978'
# target_url = 'https://www.op.gg/summoners/kr/%EC%9C%BC%EB%81%84%EC%9C%BC%EB%81%84'
response = requests.get(target_url)

print(response.text)



###########################################
print("done in %0.3fs." % (time() - start))
print(strftime('%Y-%m-%d %H:%M:%S', localtime()))





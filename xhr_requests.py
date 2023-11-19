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

script_directory = pathlib.Path().absolute()
options = Options()
options.add_argument(f"user-data-dir={script_directory}/gadgd")
options.add_experimental_option("detach", True)

# Set up any necessary configurations or options
driver = webdriver.Chrome(options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """})

driver.get('https://www.op.gg/')


with requests.Session() as s:
    selenium_user_agent = driver.execute_script("return navigator.userAgent;")
    s.headers.update({"user-agent": selenium_user_agent})
    for cookie in driver.get_cookies():
        c = {cookie['name']: cookie['value']}
        s.cookies.update(c)

# response = s.get('https://www.op.gg/summoners/kr/Levid')
response = s.get('https://www.op.gg/summoners/kr/apm50')
# response = s.get('https://op.gg/api/v1.0/internal/bypass/games/kr/summoners/5mt_C7wXXObgsbnYcFaTx8gqmeobClLHnGiYH49RyINWU7Y?&limit=20&hl=ko_KR&game_type=soloranked')

r_status = response.status_code
r_json = response.content.decode('utf-8')

# with open('asdfasdfasdf.txt', 'w', encoding='utf-8') as file:
#     file.write((r_json))

print(r_status)
# print(type(r_status))
# print(r_json)
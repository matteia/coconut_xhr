import os
import time
import pathlib
import json

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
options.add_argument(f"user-data-dir={script_directory}/selenium_prof")
options.add_experimental_option("detach", True)

# Set up any necessary configurations or options
driver = webdriver.Chrome(options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """})


start = time()
print(strftime('%Y-%m-%d %H:%M:%S', localtime()))
print('\n')





target_url = 'https://www.op.gg/summoners/kr/%EB%AF%B8%EB%A5%B5%EB%B6%88%EC%83%81'

driver.get(target_url)

page_source = driver.page_source

print(page_source)









print("done in %0.3fs." % (time() - start))
print(strftime('%Y-%m-%d %H:%M:%S', localtime()))
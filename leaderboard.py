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


from datetime import date, timedelta, datetime
####### END OF IMPORTS #########

foldername = '../soloq_scrape/scraped_results/'
text_files = glob.glob(f'{foldername}*.txt')
print(len(text_files))
# print(*sorted(text_files))


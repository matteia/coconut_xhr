import os
import time
import pathlib
import asyncio

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

###### some custom functions

async def wait_presence(ddriver, xpath):
    WebDriverWait(ddriver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))


async def wait_visibility(ddriver, xpath):
    WebDriverWait(ddriver, 10).until(EC.visibility_of_any_elements_located((By.XPATH, xpath)))


async def show_more_history(ddriver, xpath):
    await wait_presence(ddriver, xpath)
    await wait_visibility(ddriver, xpath)
    show_more_history_button = WebDriverWait(ddriver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    return show_more_history_button


async def dr_execute_script(ddriver, xpath):
    button = await show_more_history(ddriver, xpath)
    ddriver.execute_script("arguments[0].click()", button)
    return button


async def dr_execute_script2(ddriver, xpath):
    task1 = asyncio.create_task(wait_presence(ddriver, xpath))
    task2 = asyncio.create_task(wait_visibility(ddriver, xpath))
    task3 = asyncio.create_task(show_more_history(ddriver, xpath))

    await task1
    await task2
    button = await task3

    ddriver.execute_script("arguments[0].click()", button)


######################################


start = time()
print(strftime('%Y-%m-%d %H:%M:%S', localtime()))
print('\n')



script_directory = pathlib.Path().absolute()

# start_url = 'https://www.op.gg'
# start_url = 'https://www.op.gg/leaderboards/tier?page=1'
target_url = 'https://www.op.gg/summoners/kr/%EC%9C%BC%EB%81%84%EC%9C%BC%EB%81%84'   ### 으끄으끄
# target_url = 'https://www.op.gg/summoners/kr/' + '으끄으끄'   ### 으끄으끄
# target_url = 'https://www.op.gg/summoners/kr/%EB%AF%B8%EB%A5%B5%EB%B6%88%EC%83%81'

options = Options()
options.add_argument(f"user-data-dir={script_directory}/sele_profiles/selenium_prof")
# options.add_argument(f"user-data-dir={script_directory}/sele_profiles/rtrtr")
options.add_experimental_option("detach", True)
options.add_argument("--headless=new")

# Set up any necessary configurations or options
driver = webdriver.Chrome(options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """})

driver.get(target_url)

only_soloq_xpath = '//*[@id="content-container"]/div[2]/div[1]/ul/li[2]/button'
only_soloq_button = driver.find_element(By.XPATH, only_soloq_xpath)
only_soloq_button.click()


show_more_history_xpath = '//*[@id="content-container"]/div[2]/button'




i = 0
while i < 20:
    print(f'i: {i}')
    try:
        asyncio.run(dr_execute_script2(driver, show_more_history_xpath))
        sleep(0.03)
        i += 1
    except:
        print('end reached')


divs_xpath = '//*[@id="content-container"]/div[2]/div[3]'
divs = driver.find_element(By.XPATH, divs_xpath)
divs_html = divs.get_attribute('outerHTML')

soup = BeautifulSoup(divs_html, 'html.parser')
divs = soup.find_all('div', {"result"})
divs_len = len(divs)

print(f'first round done: {divs_len}')

additional_clicks = int((380 - divs_len)/20 * 1.5)

if divs_len < 300:
    print('not long enough')
    print(f'additional_clicks: {additional_clicks}')
    i = 0
    while i < additional_clicks:
        print(f'i: {i}')
        try:
            asyncio.run(dr_execute_script2(driver, show_more_history_xpath))
            sleep(0.02)
            i += 1
        except:
            print('end reached')

else:
    print('long enough')


divs = driver.find_element(By.XPATH, divs_xpath)
divs_html = divs.get_attribute('outerHTML')

soup = BeautifulSoup(divs_html, 'html.parser')
divs = soup.find_all('div', {"result"})
divs_len = len(divs)

# print(f'second round done: {divs_len}')
# if divs_len < 300:
#     print('not long enough')
#     i = 0
#     while i < 5:
#         try:
#             asyncio.run(dr_execute_script2(driver, show_more_history_xpath))
#             sleep(0.05)
#             i += 1
#         except:
#             print('end reached')
#
# else:
#     print('long enough')

for div in divs:
    game_result = div.text
    print(game_result)

print(f'final divs length: {divs_len}')

print("done in %0.3fs." % (time() - start))
print(strftime('%Y-%m-%d %H:%M:%S', localtime()))


sleep(10000)


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

start = time()
print(strftime('%Y-%m-%d %H:%M:%S', localtime()))
print('\n')


script_directory = pathlib.Path().absolute()

# start_url = 'https://www.op.gg'
start_url = 'https://www.op.gg/leaderboards/tier?region=kr&page='

tbody_xpath = '//*[@id="content-container"]/div[3]/table/tbody'
tbody_selector = '#content-container > div.css-1v7j0iq.efbuh0u2 > table > tbody'


options = Options()
# options.add_argument(f"user-data-dir={script_directory}/selenium_prof")
options.add_argument(f"user-data-dir={script_directory}/uuuuu")

# Set up any necessary configurations or options
driver = webdriver.Chrome(options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """})

# leaderboard_filename = 'leaderboard_part_3.txt'
# leaderboard_file = open(leaderboard_filename, 'wb')

star_page_number = 17010
target_page_number = star_page_number + 100  ### done in 192.029s. (100 pages)

#### DONE PAGES
### 0~100(1), 100~200(2), 200~300(3),


gamers = []
for i in range(star_page_number, target_page_number):
    driver.get(start_url+str(i+1))

    driver.implicitly_wait(3)

    # WebDriverWait(driver, 10).until(EC.visibility_of_any_elements_located((By.XPATH, tbody_xpath)))
    # tbody = driver.find_element(By.XPATH, tbody_xpath)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, tbody_selector)))
    tbody = driver.find_element(By.CSS_SELECTOR, tbody_selector)

    tbody_html = tbody.get_attribute('outerHTML')

    soup = BeautifulSoup(tbody_html, 'html.parser')

    tr_list = soup.find_all('tr')

    for tr in tr_list[:]:
        one_gamer = []
        ### look for tds in tr
        td_list = tr.find_all('td')
        ### id ->   .get('id')
        gamer_id = tr.get('id')

        ### tier -> [2]
        gamer_tier = td_list[2].text

        ### wins
        gamer_wins = int(td_list[-1].find('div', {'class': 'w'}).text[:-1])
        ### losses
        gamer_losses = int(td_list[-1].find('div', {'class': 'l'}).text[:-1])
        ### number of games
        gamer_games = gamer_wins + gamer_losses

        one_gamer.append(gamer_id)
        one_gamer.append(gamer_tier)
        one_gamer.append(gamer_wins)
        one_gamer.append(gamer_losses)
        one_gamer.append(gamer_games)

        gamers.append(one_gamer)

        # print(gamer_id, gamer_tier, gamer_wins, gamer_losses, gamer_games)

    sleep(0.5)

print(len(gamers))
gamers_bytes = bytes(str(gamers), 'utf-8')

# leaderboard_filename = f'leaderboard_part_3.txt'
leaderboard_filename = f'leaderboard_{star_page_number}_{target_page_number}.txt'
leaderboard_file = open(leaderboard_filename, 'wb')

leaderboard_file.write(gamers_bytes)
leaderboard_file.close()


print("done in %0.3fs." % (time() - start))
print(strftime('%Y-%m-%d %H:%M:%S', localtime()))


sleep(10000)


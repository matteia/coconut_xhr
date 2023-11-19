### using xhr approach

import os
import ast
import json
import pathlib

from urllib import parse

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

###################### END OF IMPORTS ############

script_directory = pathlib.Path().absolute()

options = Options()
options.add_argument(f"user-data-dir={script_directory}/sele_profiles/ty")
options.add_argument('--disable-application-cache')
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option("detach", True)
# options.add_argument("--headless=new")

# Set up any necessary configurations or options
driver = webdriver.Chrome(options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """})

#### timer ##############################
start = time()
print(strftime('%Y-%m-%d %H:%M:%S', localtime()))
print('\n')
##############################



filename = '../soloq_scrape/scraped_results/partitions_200plus/bronze/partition_0.txt'

with open(filename, 'rb') as f:
    one_list = f.read()

one_list = one_list.decode('utf-8')
one_list = ast.literal_eval(one_list)

player_list = [player[0] for player in one_list]
player_list = player_list[:10]
# player_list = ['미륵불상']
print(f'player_list: {player_list}')

for player in player_list:
    result_list = []
    target_url = f'https://www.op.gg/summoners/kr/{player}'

    ### move to player's opgg page
    driver.get(target_url)
    ### set script xpath
    script_xpath = '//*[@id="__NEXT_DATA__"]'


    ### try & except in case the player_name does not exist
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, script_xpath)))
        script = driver.find_element(By.XPATH, script_xpath)
        jjson = script.get_attribute('innerHTML')
        # jjson = script.get_attribute('outerHTML')

        # print(type(jjson))
        # print(jjson)

        # with open('some_json.txt', 'w', encoding='utf-8') as file:
        #     file.write(jjson)

        jjson = json.loads(jjson)

        summ_id = jjson['props']['pageProps']['data']['summoner_id']

        print(f'player: {player} // summ_id: {summ_id}')

        ended_at = ''
        ended_at = parse.quote(ended_at)

        # result_list = []
        for _ in range(20):
            # try:
            xhr_url = f'https://op.gg/api/v1.0/internal/bypass/games/kr/summoners/{summ_id}?&limit=20&hl=ko_KR&game_type=soloranked&ended_at={ended_at}'
            driver.get(xhr_url)

            json_xpath = "/html/body"
            data_json = driver.find_element(By.XPATH, json_xpath)
            data_json = data_json.text
            data_json = json.loads(data_json)

            ### jsonify received data
            # data_json = json.loads(driver.page_source)
            print(f'type(data_json): {type(data_json)}')
            ### update ended_at for querying next 20 games
            ended_at = data_json['meta']['last_game_created_at']
            print(f'ended_at: {ended_at}')
            ended_at = parse.quote(ended_at)
            print(f'ended_at: {ended_at}')


            for ddict in data_json['data']:
                result = ddict['myData']['stats']['result']
                result_list.append(result)

            # ### except in case there are no more games to load
            # except:
            #     pass


    except:
        pass



print(result_list)
print(len(result_list))

##############################
print("done in %0.3fs." % (time() - start))
print(strftime('%Y-%m-%d %H:%M:%S', localtime()))


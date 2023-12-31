### script for using opgg_xhr_fx.py in mass
## refer to scratch_5.py for glob.glob

import os
import ast
import json
import pathlib
import requests
import glob

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

from opgg_xhr_fx import xhr_scrape_player, xhr_scrape_player2, xhr_scrape_player3
from utilities import parse_result, write_player_record
from scrape_logger import scrape_logger, determine_start

###################### END OF IMPORTS ############


########################################################################################################

script_directory = pathlib.Path().absolute()

options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
options.add_argument(f"user-data-dir={script_directory}/sele_profiles/aslan")
options.add_argument('--disable-application-cache')
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option("detach", True)
# options.add_argument("--headless=new")

# Set up any necessary configurations or options
driver = webdriver.Chrome(options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """})

driver.get('https://www.op.gg/')

with requests.Session() as sel_session:
    selenium_user_agent = driver.execute_script("return navigator.userAgent;")
    sel_session.headers.update({"user-agent": selenium_user_agent})
    for cookie in driver.get_cookies():
        c = {cookie['name']: cookie['value']}
        sel_session.cookies.update(c)

# sleep(120)

#### timer ##############################
start = time()
print(strftime('%Y-%m-%d %H:%M:%S', localtime()))
print('\n')
##############################

foldername = f'{script_directory}/scraped_results'

target_files = [
                f'{foldername}/partitions_200plus/silver/partition_4',
                f'{foldername}/partitions_200plus/silver/partition_5'
                ]


for target_file in target_files:
    # print(target_file.split('/'))

    split_target_file = target_file.split('/')
    elo = split_target_file[-2]
    parti_num = int(split_target_file[-1].split('partition_')[-1])
    print(f'{elo}/partition_{parti_num}')
    # print(type(parti_num))

    # # Done: 0, 1, 2, 3, 4 // bronze
    # # Done: 0, 1,  // silver

    filename = f'{script_directory}/scraped_results/partitions_200plus/{elo}/partition_{parti_num}.txt'

    # with requests.Session() as sel_session:
    #     selenium_user_agent = driver.execute_script("return navigator.userAgent;")
    #     sel_session.headers.update({"user-agent": selenium_user_agent})
    #     for cookie in driver.get_cookies():
    #         c = {cookie['name']: cookie['value']}
    #         sel_session.cookies.update(c)

    with open(filename, 'rb') as f:
        one_list = f.read()

    one_list = one_list.decode('utf-8')
    one_list = ast.literal_eval(one_list)

    player_list = [player[0] for player in one_list]
    ### set player_list length
    player_list = player_list[:]

    print(f'player_list: {player_list}')
    print(f'len(player_lst): {len(player_list)}')

    all_records = []
    i_start = determine_start(filename)
    for i in range(i_start, len(player_list)):
        print(f'i: {i}')
        ### game results of one player
        player = player_list[i]
        # game_results = xhr_scrape_player(driver, player)
        game_results = xhr_scrape_player3(driver, sel_session, player)
        # game_results = xhr_scrape_player3(driver, sel_session, player)

        all_records.append(game_results)

        parsed_game_results = parse_result(game_results)

        ### SAVE each player record instead of appending to all_records
        ### create a function to save file ? & return filepath of saved file ?
        saved_filepath = write_player_record(filename, player, parsed_game_results)


        ### Make sure the saved file exists (scrape_logger.py)
        if os.path.exists(saved_filepath):
            scrape_logger(filename, f'{i}')

        else:
            scrape_logger(filename, f'{i}-e')


    for i in range(len(all_records)):
        all_records[i] = parse_result(all_records[i])


    ##############################
    print("done in %0.3fs." % (time() - start))
    print(strftime('%Y-%m-%d %H:%M:%S', localtime()))

    sleep(323)

### shut down upon completion
os.system('shutdown -s')


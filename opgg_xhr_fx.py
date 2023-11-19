### function for scraping player record using xhr & summoner id

import os
import ast
import json
import pathlib

from urllib import parse

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

from opgg_one_player_fx import scrape_one_player
from utilities import parse_result, write_player_record
from scrape_logger import scrape_logger, determine_start

###################### END OF IMPORTS ############



def xhr_scrape_player(driver, player):
    result_list = []
    first_url = f'https://www.op.gg/summoners/kr/{player}'

    ### move to player's opgg page
    driver.get(first_url)

    ### set script xpath
    script_xpath = '//*[@id="__NEXT_DATA__"]'

    ### try & except in case the player_name does not exist
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, script_xpath)))
        script = driver.find_element(By.XPATH, script_xpath)
        jjson = script.get_attribute('innerHTML')

        jjson = json.loads(jjson)

        summ_id = jjson['props']['pageProps']['data']['summoner_id']

        print(f'player: {player} // summ_id: {summ_id}')

        ended_at = ''
        ended_at = parse.quote(ended_at)

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

            ### update ended_at for querying next 20 games
            ended_at = data_json['meta']['last_game_created_at']

            ended_at = parse.quote(ended_at)


            for ddict in data_json['data']:
                result = ddict['myData']['stats']['result']
                result_list.append(result)



    except:
        pass
    sleep(0.5)
    print(len(result_list))
    return result_list


### this function uses requests with session, cookies, headers, etc
def xhr_scrape_player2(driver, sel_session, player):
    result_list = []
    first_url = f'https://www.op.gg/summoners/kr/{player}'

    ### move to player's opgg page
    driver.get(first_url)

    ### set script xpath
    script_xpath = '//*[@id="__NEXT_DATA__"]'

    ### try & except in case the player_name does not exist
    try:
        WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.XPATH, script_xpath)))
        script = driver.find_element(By.XPATH, script_xpath)
        jjson = script.get_attribute('innerHTML')

        jjson = json.loads(jjson)

        summ_id = jjson['props']['pageProps']['data']['summoner_id']

        print(f'player: {player} // summ_id: {summ_id}')

        ended_at = ''
        ended_at = parse.quote(ended_at)

        for _ in range(20):
            # try:
            xhr_url = f'https://op.gg/api/v1.0/internal/bypass/games/kr/summoners/{summ_id}?&limit=20&hl=ko_KR&game_type=soloranked&ended_at={ended_at}'
            response = sel_session.get(xhr_url)

            data_json = response.json()

            ### update ended_at for querying next 20 games
            ended_at = data_json['meta']['last_game_created_at']

            ended_at = parse.quote(ended_at)


            for ddict in data_json['data']:
                result = ddict['myData']['stats']['result']
                result_list.append(result)



    except:
        pass
    sleep(0.5)
    print(len(result_list))
    return result_list


### this function uses requests with session, cookies, headers, etc & deals with error 429
def xhr_scrape_player3(driver, sel_session, player):
    result_list = []
    def request_loop(some_url):
        rresponse = sel_session.get(some_url)
        status_code = rresponse.status_code

        if status_code == 429:
            print(f'\n status_code: {status_code}', end='')
            sleep(10)
            return request_loop(some_url)
        elif status_code == 200:
            # print(f'status_code: {status_code}')
            # result_json = rresponse.json()
            return rresponse
        elif status_code == 422:
            print(f'\n status_code: {status_code}', end='')
            # result_json = rresponse.json()
            return rresponse
        else:
            print(f'\n status_code: {status_code}', end='')


    first_url = f'https://www.op.gg/summoners/kr/{player}'

    try:

        ### requests.get first url and find summ id
        # first_page_res = sel_session.get(first_url)
        first_page_res = request_loop(first_url)
        first_status_code = first_page_res.status_code
        first_string = first_page_res.content.decode('utf-8')

        ### create soup
        soup = BeautifulSoup(first_string, 'html.parser')

        ### find the div with script in it & convert to dict
        script_div = soup.find('script', type='application/json')
        script_div = json.loads(script_div.string)

        summ_id = script_div['props']['pageProps']['data']['summoner_id']

        ### try & except in case the player_name does not exist

        print(f'player: {player} // summ_id: {summ_id}')

        ended_at = ''
        ended_at = parse.quote(ended_at)


        for ii in range(20):
            # print(f'{ii+1}/20', end=' \r')
            print(f'\r xhr:{ii+1}/20', end='')
            try:
                xhr_url = f'https://op.gg/api/v1.0/internal/bypass/games/kr/summoners/{summ_id}?&limit=20&hl=ko_KR&game_type=soloranked&ended_at={ended_at}'
                xhr_response = request_loop(xhr_url)

                if xhr_response.status_code == 422:
                    break

                data_json = xhr_response.json()


                ### update ended_at for querying next 20 games
                ended_at = data_json['meta']['last_game_created_at']
                # print(ended_at)
                # print(type(ended_at))
                ended_at = parse.quote(ended_at)


                for ddict in data_json['data']:
                    result = ddict['myData']['stats']['result']
                    result_list.append(result)

            except:
                pass

    except KeyError:
        pass

    sleep(0.5)

    print(f'\n {len(result_list)}')
    return result_list


########################################################################################################
########################################################################################################

# script_directory = pathlib.Path().absolute()
#
# options = Options()
# options.add_argument(f"user-data-dir={script_directory}/sele_profiles/ty")
# options.add_argument('--disable-application-cache')
# options.add_experimental_option("useAutomationExtension", False)
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# # options.add_experimental_option("detach", True)
# # options.add_argument("--headless=new")
#
# # Set up any necessary configurations or options
# driver = webdriver.Chrome(options=options)
# driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """})
#
#
# #### timer ##############################
# start = time()
# print(strftime('%Y-%m-%d %H:%M:%S', localtime()))
# print('\n')
# ##############################
#
#
#
# filename = '../soloq_scrape/scraped_results/partitions_200plus/bronze/partition_0.txt'
#
# with open(filename, 'rb') as f:
#     one_list = f.read()
#
# one_list = one_list.decode('utf-8')
# one_list = ast.literal_eval(one_list)
#
# player_list = [player[0] for player in one_list]
# player_list = player_list[:30]
#
# print(f'player_list: {player_list}')
# print(f'len(player_lst): {len(player_list)}')
#
# all_records = []
# i_start = determine_start(filename)
# for i in range(i_start, len(player_list)):
#     print(i)
#     ### game results of one player
#     player = player_list[i]
#     game_results = xhr_scrape_player(driver, player)
#
#     all_records.append(game_results)
#
#     parsed_game_results = parse_result(game_results)
#
#     ### SAVE each player record instead of appending to all_records
#     ### create a function to save file ? & return filepath of saved file ?
#     saved_filepath = write_player_record(filename, player, parsed_game_results)
#
#     # with open(f'../soloq_scrape/scraped_results/parsed_200plus/bronze/{player}.txt', 'w') as file:
#     #     file.write(str(parsed_game_results))
#
#     ### Make sure the saved file exists (scrape_logger.py)
#     if os.path.exists(saved_filepath):
#         scrape_logger(filename, f'{i}')
#
#     else:
#         scrape_logger(filename, f'{i}-e')
#
#     ### filepath = parsed_200plus > bronze > {player_name.txt}
#     # if saved_filename exists:
#     #     log(i)
#     ### filepath = parsed_200plus > logs > bronze > 'partition_X.txt' > content: 0,1,2,3,4,5,6,7, .... (.txt?)
#
#
#
#
# # for player in player_list:
# #     all_records.append(xhr_scrape_player(driver, player))
#
#
# # print(all_records)
#
#
# for i in range(len(all_records)):
#     all_records[i] = parse_result(all_records[i])
#
#
# ##############################
# print("done in %0.3fs." % (time() - start))
# print(strftime('%Y-%m-%d %H:%M:%S', localtime()))


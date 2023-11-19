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


# player_list = [['으끄으끄']]
player_list = [['마스터가면계삭함', 'master', 287, 278, 565], ['levid', 'master', 303, 297, 600], ['하무요', 'master', 136, 116, 252], ['평화로운협곡원해', 'master', 149, 130, 279], ['빠가사리카롱', 'master', 178, 175, 353], ['혜지uwu', 'master', 197, 206, 403], ['긍정용기', 'master', 192, 179, 371], ['benecian', 'master', 295, 285, 580], ['내꿈은롤드컵', 'master', 211, 173, 384], ['박예근김보성', 'master', 150, 124, 274], ['nomapreading', 'master', 189, 190, 379], ['살인전차는달린다', 'master', 322, 343, 665], ['이슬공쥬최고', 'master', 256, 247, 503], ['완숙반숙여인숙', 'master', 185, 180, 365], ['애니비효', 'master', 169, 158, 327], ['나둬', 'master', 115, 114, 229], ['에키클리마', 'master', 126, 120, 246], ['소나해', 'master', 107, 104, 211], ['revelredflavor', 'master', 147, 142, 289], ['액쇼니', 'master', 143, 134, 277]]

summ_id_list = []

# target_url = 'https://www.op.gg/summoners/kr/%EB%AF%B8%EB%A5%B5%EB%B6%88%EC%83%81'
# target_url = 'https://www.op.gg/summoners/kr/으끄으끄'
for player in player_list:
    player_name = player[0]
    target_url = f'https://www.op.gg/summoners/kr/{player_name}'


    driver.get(target_url)


    script_xpath = '//*[@id="__NEXT_DATA__"]'
# jjson_xpath = '//*[@id="__NEXT_DATA__"]/text()'
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
        # game_name = jjson['props']['pageProps']['data']['name']

        print(summ_id)
        summ_id_list.append(summ_id)
        # print(game_name)

    except:
        pass




print(summ_id_list)
print(len(summ_id_list))





print("done in %0.3fs." % (time() - start))
print(strftime('%Y-%m-%d %H:%M:%S', localtime()))
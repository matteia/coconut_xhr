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
options.add_argument(f"user-data-dir={script_directory}/selenium_prof")
options.add_experimental_option("detach", True)

# Set up any necessary configurations or options
driver = webdriver.Chrome(options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """})


start = time()
print(strftime('%Y-%m-%d %H:%M:%S', localtime()))
print('\n')


player_list = ['15I9tClNoonQe_93NOr5ei4l_H0lq68EVDNNB0Xbud6EdEnmA4Mfxq1TXw', 'LvWzOQrwmyPYrPLNCXriMTWJ2lgtJwDZ1QjFjdIXlVvZkeMN2eStPO0ucg', 'Dh1s_9SrEAek0FdfKcpQIzezh12QwMmRldrXeoB5BhbHNgvb', 'r-YrNmRjhU8A47bNcZ02cuo9ZW1zYvNI6ImQdim7JbLWXGE', 'oUaE5er_EVRj9MO80GABxX0AFXmo2cG-Y4xd0BWbNdg2etE', 'e254vgFufIcE-xzodD6iOQUl5xb3wNZHUOIficBIaEPCQYU', '4G-iMvaTHQ5d-EwqZsQ2PnQURcz_PEcOZqsO-i4CDrRTgGU', 'rguKB7cC6S9ydz3QTgPgsYwvtbRbMd41x5kZqSdcBrCwrmI', 'yJG-ISWJs02Qp-XCKekKrFwoWIIbdfRzBS-0RzqrRGUcgkQ', 'yAIiSIVtsFO9TXHrn0PbGkpj-h1MYNdJF38GysJ42RRPZxM', 'J317TRm1rhDs-xKNP9gwCcXh8gStAg8yo5vGzesPzI9nqg', 'mAVwzcYZ4WVTAmSVslXo28iXtMk7qdfK7toA8bOsh1qq_-k', 'MmY9XsoNWoh4RHkiGwl0ShvDaeE44daBUhrw2pTaDECZ1Q', 'qELBxkENQxgUiUrxTD1_RYJzuW4wIIIeBi2yrF5WZoC0fQ', 'HxoihXpYbI2gzQuhQPa4qCurgWBGzjNyYv7nlhHMonaVXg', '-fs0BWRHGdrRyY_XCEsropYljuj1WI5hJ8aDsusEM4Ai05s', 'M4xWCLRGWMl0GNJdvjDfcAG_VR7FkrCGUWG6JvEHP_H0pTs', '4P6mMSsMa1w8U4DvUBhNEzrznpk8_1kB89ysfYZRS_OqIlY', 'oUg313Y_eF5_7kugkdJW9XWTsrBhmZ5GakY86EQwLlkoCyE']
player_list = ['EwS62Qn1RuxFkIngUEltKx-ReARJ4HZo6WB96WG4TB2kFQc']

# for _ in range(1):
for summ_id in player_list:
    # target_url = f'https://op.gg/api/v1.0/internal/bypass/games/kr/summoners/{summ_id}?&limit=20&hl=ko_KR&game_type=soloranked'
    target_url = f'https://op.gg/api/v1.0/internal/bypass/games/kr/summoners/{summ_id}?&limit=20&hl=ko_KR&game_type=soloranked&ended_at='

    driver.get(target_url)

    json_xpath = "/html/body"
    # data_json = driver.page_source
    data_json = driver.find_element(By.XPATH, json_xpath)
    data_json = data_json.text
    print(data_json)
    print(type(data_json))
    data_json = json.loads(data_json)
    print(type(data_json))


print("done in %0.3fs." % (time() - start))
print(strftime('%Y-%m-%d %H:%M:%S', localtime()))
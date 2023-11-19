### utilizing opgg_one_player2.py

import os
import ast
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


def scrape_one_player(driver, player_name):

    base_url = 'https://www.op.gg/summoners/kr/'

    ### set target_url with player name
    target_url = base_url + player_name

    try:
        ### move to target_url
        driver.get(target_url)

        ### find and click only soloq history button
        only_soloq_xpath = '//*[@id="content-container"]/div[2]/div[1]/ul/li[2]/button'
        only_soloq_button = driver.find_element(By.XPATH, only_soloq_xpath)
        only_soloq_button.click()

        show_more_history_xpath = '//*[@id="content-container"]/div[2]/button'

        i = 0
        while i < 30:
            # print(f'i: {i}')
            try:
                asyncio.run(dr_execute_script2(driver, show_more_history_xpath))
                sleep(0.03)
                i += 1
            except:
                pass

        divs_xpath = '//*[@id="content-container"]/div[2]/div[3]'
        divs = driver.find_element(By.XPATH, divs_xpath)
        divs_html = divs.get_attribute('outerHTML')

        soup = BeautifulSoup(divs_html, 'html.parser')
        divs = soup.find_all('div', {"result"})
        divs_len = len(divs)

        ### calculate additional clicks
        additional_clicks = int((380 - divs_len) / 20 * 1.5)

        if divs_len < 300:
            # print('not long enough')
            # print(f'additional_clicks: {additional_clicks}')
            i = 0
            while i < additional_clicks:
                # print(f'i: {i}')
                try:
                    asyncio.run(dr_execute_script2(driver, show_more_history_xpath))
                    sleep(0.02)
                    i += 1
                except:
                    pass
                    # print('end reached')

        divs = driver.find_element(By.XPATH, divs_xpath)
        divs_html = divs.get_attribute('outerHTML')

        soup = BeautifulSoup(divs_html, 'html.parser')
        divs = soup.find_all('div', {"result"})
        divs_len = len(divs)

        ### parse game results from divs
        game_results = []

        for div in divs:
            game_result = div.text.strip()
            # print(game_result)
            if game_result == '승리':
                game_results.append(1)
            elif game_result == 'WIN':
                game_results.append(1)
            elif game_result == '패배':
                game_results.append(0)
            elif game_result == 'LOSE':
                game_results.append(0)
            elif game_result == '다시하기':
                game_results.append(999)
            elif game_result == 'REMAKE':
                game_results.append(999)

        for res in game_results:
            if res == 999:
                game_results.remove(res)

        return game_results
    except NoSuchElementException:
        return []

    # ### move to target_url
    # driver.get(target_url)
    #
    # ### find and click only soloq history button
    # only_soloq_xpath = '//*[@id="content-container"]/div[2]/div[1]/ul/li[2]/button'
    # only_soloq_button = driver.find_element(By.XPATH, only_soloq_xpath)
    # only_soloq_button.click()
    #
    # show_more_history_xpath = '//*[@id="content-container"]/div[2]/button'
    #
    # i = 0
    # while i < 30:
    #     # print(f'i: {i}')
    #     try:
    #         asyncio.run(dr_execute_script2(driver, show_more_history_xpath))
    #         sleep(0.03)
    #         i += 1
    #     except:
    #         pass
    #
    # divs_xpath = '//*[@id="content-container"]/div[2]/div[3]'
    # divs = driver.find_element(By.XPATH, divs_xpath)
    # divs_html = divs.get_attribute('outerHTML')
    #
    # soup = BeautifulSoup(divs_html, 'html.parser')
    # divs = soup.find_all('div', {"result"})
    # divs_len = len(divs)
    #
    # ### calculate additional clicks
    # additional_clicks = int((380 - divs_len) / 20 * 1.5)
    #
    # if divs_len < 300:
    #     # print('not long enough')
    #     # print(f'additional_clicks: {additional_clicks}')
    #     i = 0
    #     while i < additional_clicks:
    #         # print(f'i: {i}')
    #         try:
    #             asyncio.run(dr_execute_script2(driver, show_more_history_xpath))
    #             sleep(0.02)
    #             i += 1
    #         except:
    #             pass
    #             # print('end reached')
    #
    # divs = driver.find_element(By.XPATH, divs_xpath)
    # divs_html = divs.get_attribute('outerHTML')
    #
    # soup = BeautifulSoup(divs_html, 'html.parser')
    # divs = soup.find_all('div', {"result"})
    # divs_len = len(divs)
    #
    # ### parse game results from divs
    # game_results = []
    #
    # for div in divs:
    #     game_result = div.text.strip()
    #     # print(game_result)
    #     if game_result == '승리':
    #         game_results.append(1)
    #     elif game_result == 'WIN':
    #         game_results.append(1)
    #     elif game_result == '패배' or game_result == 'WIN':
    #         game_results.append(0)
    #     elif game_result == 'LOSE':
    #         game_results.append(0)
    #     elif game_result == '다시하기':
    #         game_results.append(999)
    #     elif game_result == 'REMAKE':
    #         game_results.append(999)
    #
    # for res in game_results:
    #     if res == 999:
    #         game_results.remove(res)
    #
    #
    # return game_results





################################

# filename = '../soloq_scrape/scraped_results/partitions_200plus/bronze/partition_0.txt'
#
# result = scrape_one_player(filename)
#
# print(result)
#
#

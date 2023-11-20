### script for logging scraping progress for each partition
### output : origin_file, completed index,

import os
import ast
import pathlib


########### END OF IMPORTS ##############

script_directory = pathlib.Path().absolute()

def scrape_logger(filepath, iindex):
    elo = filepath.split('/')[-2]
    filename = filepath.split('/')[-1].split('.')[0]
    log_filepath = f'{script_directory}/scraped_results/parse_logs/{elo}/{filename}/scrape_log.txt'

    with open(log_filepath, 'a') as file:
        file.write(f'{iindex}, ')



    return None


def determine_start(filepath):
    elo = filepath.split('/')[-2]
    filename = filepath.split('/')[-1].split('.')[0]
    log_filepath = f'{script_directory}/scraped_results/parse_logs/{elo}/{filename}/scrape_log.txt'

    if os.path.exists(log_filepath):
        with open(log_filepath, 'r') as file:
            log_content = file.read()

        log_content = list(ast.literal_eval(log_content))
        i_start = max(log_content) + 1
    else:
        i_start = 0

    return i_start



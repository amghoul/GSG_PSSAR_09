import os
import sys
import logging
from loading_saving import load_data, save_df_to_csv
from clean import clean_chess, who_clean
from statistics_calc import get_df_stats, get_column_stats
from questions_answers import *

log = logging.getLogger(__name__)

if __name__ == "__main__":
    csv_save_raw = os.path.join("data","raw")
    csv_save_processed = os.path.join("data","processed")
    name_ds_chess="chess_games"
    name_ds_who="who_data"
    chart_save_path = os.path.join("output","charts")
    
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    
    chess_url = 'https://drive.google.com/file/d/1eR3NZtwIC6ECN3vhtrynqmx8okG0twA7/view'
    WHO_URL = 'https://github.com/Priyankkoul/Life-Expectancy-WHO---Data-Analytics/blob/master/DATASET.csv?raw=true'
    chess_raw = load_data(chess_url, os.path.join(csv_save_raw, name_ds_chess + "_raw.csv"), log)
    who_raw = load_data(WHO_URL, os.path.join(csv_save_raw, name_ds_who + "_raw.csv"), log)

    ################ Cleaning
    chess_raw_copy = chess_raw.copy()
    who_raw_copy = who_raw.copy()

    #get_df_stats(chess_raw)
    clean_chess = clean_chess(chess_raw_copy)
    log.info(f"Chess dataset cleaned successfully")
    #get_df_stats(who_raw)
    clean_who = who_clean(who_raw_copy)
    log.info(f"WHO dataset cleaned successfully")
    save_df_to_csv(clean_chess,os.path.join(csv_save_processed,name_ds_chess + "_processed.csv" ), log)
    save_df_to_csv(clean_who, os.path.join(csv_save_processed, name_ds_who + "_processed.csv"), log)

    chess_clean_copy = clean_chess.copy()
    who_clean_copy = clean_who.copy()
    
    q1(chess_clean_copy, log)
    q2(chess_clean_copy, chart_save_path , log)
    q3(who_clean_copy, log)
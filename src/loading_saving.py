import os
import pandas as pd
import gdown
import logging

def load_data(url: str, local_path: str, log: logging.Logger) -> pd.DataFrame:
    """Load from a URL using gdown to bypass warning screens, 
    save locally, and return as a DataFrame."""
    
    if os.path.exists(local_path):
        log.info(f'Loading from cache: {local_path}')
        return pd.read_csv(local_path)
    
    log.info(f'Downloading from the url to {local_path}...')
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    
    gdown.download(url, local_path, quiet=False)
    
    log.info('Download complete. Reading into DataFrame...')
    return pd.read_csv(local_path)

def save_df_to_csv(df: pd.DataFrame, path: str, log: logging.Logger)-> None:
    """This function save a datafram to a csv file 
    """
    df.to_csv(path, index=False)
    log.info(f"Dataframe successfully saved to: {path}")
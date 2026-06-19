import pandas as pd
import numpy as np
import logging

def get_df_stats(df: pd.DataFrame, log: logging.Logger)-> None:
    """This function takes a dataframe and print its statistics
    """
    stats_list = ["dtypes", "describe", "isnull", "duplicated", "columns","shape"]
    for item in stats_list:
        print(f"\n############ df.{item} ############")
        attr = getattr(df, item)
        if item in ["describe"]:
            print(attr())
        elif item == "isnull":
            print(attr().sum())
        elif item == "duplicated":
            print(attr().sum())
        else:
            print(attr)

def get_column_stats(df: pd.DataFrame, col_name: str, log: logging.Logger)-> dict:
    print(f"\nDescriptive statistics profile of chess {col_name}:")
    stats_keys = ["shape", "describe", "mean", "median", "iqr", "skew"]
    stat_dict = {key: None for key in stats_keys}
    for key in stat_dict.keys():
        if key in ["shape"]:
            attr = getattr(df[col_name], key)
            stat_dict[key] = attr
            print(f"    --> {key.capitalize()}: {stat_dict[key]}")
        elif key in ["iqr"]:
            attr = getattr(df[col_name], 'quantile')
            stat_dict[key] = attr(0.75) - attr(0.25)
            print(f"    --> {key.capitalize()}: {stat_dict[key]:.2f}")
        else:
            attr = getattr(df[col_name], key)
            stat_dict[key] = attr()
            if key in ['describe']:
                print(f"    --> {key.capitalize()}: ")
                print(f"    --> {stat_dict[key]}")
            else:
                print(f"    --> {key.capitalize()}: {stat_dict[key]:.2f}")
    return stat_dict

import pandas as pd
from statistics import get_df_stats, get_column_stats
import logging
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


def q1(df: pd.DataFrame, log: logging.Logger)-> None: 
    """
    Answer AQ1:Descriptive statistics profile of chess turns & rating_diff
    for turns:
    Descriptive statistics profile of chess turns:
    --> Shape: (20058,)
    --> Describe: 
    --> count    20058.000000
        mean        60.465999
        std         33.570585
        min          1.000000
        25%         37.000000
        50%         55.000000
        75%         79.000000
        max        349.000000
        Name: turns, dtype: float64
    --> Mean: 60.47
    --> Median: 55.00
    --> Iqr: 42.00
    --> Skew: 0.90
    Mean (60.47) > Median (55.0) confirms right skew — some very long games pull the average up
    A skewness value of 0.9 indicates that your dataset is moderately asymmetrical with a long tail on the right side, 
    meaning the majority of your observations are concentrated below the statistical mean

    for rating_diff:
    Descriptive statistics profile of chess rating_diff:
    --> Shape: (20058,)
    --> Describe: 
    --> count    20058.000000
        mean       173.091435
        std        179.214854
        min          0.000000
        25%         45.000000
        50%        115.000000
        75%        241.000000
        max       1605.000000
        Name: rating_diff, dtype: float64
    --> Mean: 173.09
    --> Median: 115.00
    --> Iqr: 196.00
    --> Skew: 1.95
    Most chess matches are close, with half of the games having a rating gap under 115 points. 
    However, a few rare games pair players with massive skill differences. 
    These extreme mismatches create a long tail in the data (right skew), 
    which drags the overall average up to 173 points and shows that matchmaking can sometimes be highly flexible.
    """
    turns_stat_dict = get_column_stats(df, 'turns', log)
    df['rating_diff'] = abs(df['white_rating'] - df['black_rating'])
    rating_diff_stat_dict = get_column_stats(df, 'rating_diff', log)

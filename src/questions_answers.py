import pandas as pd
import numpy as np
import os
from statistics import get_df_stats, get_column_stats
import logging
import matplotlib.pyplot as plt
#import seaborn as sns
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
    A skewness value of 0.9 indicates that the dataset is moderately asymmetrical with a long tail on the right side, 
    meaning the majority of the observations are concentrated below the statistical mean

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
    log.info("################ Q1 answering:")
    turns_stat_dict = get_column_stats(df, 'turns', log)
    df['rating_diff'] = abs(df['white_rating'] - df['black_rating'])
    rating_diff_stat_dict = get_column_stats(df, 'rating_diff', log)

def q2(df: pd.DataFrame, path: str, log: logging.Logger)-> None:
    """AQ2: Distribution analysis — normality tests, log-transform
    # ################ Q2 answering: The charts are in output/charts path
    # --------> Q2 answering for turns:
    # Shapiro-Wilk p = 0.000000
    # Original skew: 0.90
    # Log skew: -1.61
    # SQRT skew: -0.06
    # --------> Q2 answering for rating_diff:
    # Shapiro-Wilk p = 0.000000
    # Original skew: 1.95
    # Log skew: -0.90
    # SQRT skew: 0.62
    1. Shapiro-Wilk p = 0.000000 (Strictly Non-Normal)A p-value of 0.000000 (which is less than 0.05) 
    means the dataset fails the normality test completely. 
    You can be 100% certain that the game length data does not form a perfect, symmetrical bell curve.
    2. Original skew: 0.90 (Moderately Right-Skewed)Your raw data has a moderate positive skew. This means most chess games finish relatively quickly, but a handful of exceptionally long games pull a long tail out to the right.
    3. Log skew: -1.61 s a strong negative (left) skew.This means the log transformation squished the long right tail too much and dragged a long, artificial tail out to the left instead.
    4. SQRT skew: -0.06 (Perfect Symmetry) While the Log transformation over-corrected the data, 
    the Square Root transformation compressed the long right-hand tail with perfect precision. 
    A value this close to 0 means the left side and right side of the transformed distribution are now almost mirror images of each other.
    
    Here is the formal statistical analysis for the rating_diff output, following the template structure:
    1- Shapiro-Wilk p = 0.000000 (Strictly Non-Normal) 
    A p-value of 0.000000 (which is less than 0.05) means the dataset fails the normality test completely. 
    You can be 100% certain that the player rating difference data does not form a perfect, 
    symmetrical bell curve.
    2- Original skew: 1.95 (Highly Right-Skewed)Your raw data has a severe positive skew. 
    This means most chess matches are closely contested with small rating gaps, 
    but a small handful of extreme matchmaking mismatches pull a very long, heavy tail out to the right.
    3- Log skew: -0.90 (Moderately Left-Skewed)This indicates a moderate negative skew. 
    While it brought the number down, the log transformation was too aggressive, over-correcting the long 
    right tail and dragging a new, artificial tail out to the left instead.
    4- SQRT skew: 0.62 (Moderately Right-Skewed)While the Log transformation over-corrected the data into 
    a negative shape, the Square Root transformation compressed the tail more gently. 
    A value of 0.62 means the data is still slightly right-skewed, but it is much closer to symmetry than 
    the original raw data
    """
    log.info(f"################ Q2 answering:") 
    col_name= 'turns'
    chart_full_path = os.path.join(path, 'Q2_'+col_name+'_dist.png')
    q2_for_column(df, col_name, chart_full_path,log)

    df['rating_diff'] = abs(df['white_rating'] - df['black_rating'])
    col_name= 'rating_diff'
    chart_full_path = os.path.join(path, 'Q2_'+col_name+'_dist.png')
    q2_for_column(df, col_name, chart_full_path, log)

def q2_for_column(df: pd.DataFrame, col_name: str, path: str, log: logging.Logger):
    log.info(f"--------> Q2 answering for {col_name}:") 
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df[col_name], bins=50, color='#1B3A2D', edgecolor='white', linewidth=0.3)
    ax.axvline(df[col_name].mean(), color='#C9A84C', lw=2, label=f"Mean: {df[col_name].mean():.0f}")
    ax.axvline(df[col_name].median(), color='#E8C96A', lw=2, ls='--', label=f"Median: {df[col_name].median():.0f}")
    if col_name == 'turns':
        ax.set_xlabel("Number of Turns (Moves)", fontsize=11)
        ax.set_ylabel("Number of Games (Frequency)", fontsize=11)
        ax.set_title("Distribution of Chess Game Lengths (Turns)", fontsize=14, fontweight='bold', pad=15)
    else:
        ax.set_xlabel("Rating Difference", fontsize=11)
        ax.set_ylabel("Number of Games (Frequency)", fontsize=11)
        ax.set_title("Distribution of Player Rating Differences", fontsize=14, fontweight='bold', pad=15)
        
    ax.legend()
    plt.savefig(path, dpi=150)
    
    stat, p = stats.shapiro(df[col_name].sample(1000, random_state=42))
    log.info(f"Shapiro-Wilk p = {p:.6f}") 
    if col_name == 'turns':
        df[col_name+'_log'] = np.log(df[col_name])
    else:
        df[col_name+'_log'] = np.log1p(df[col_name])
    df[col_name+'_sqrt'] = np.sqrt(df[col_name])
    log.info(f"Original skew: {df[col_name].skew():.2f}") 
    log.info(f"Log skew: {df[col_name+'_log'].skew():.2f}") 
    log.info(f"SQRT skew: {df[col_name+'_sqrt'].skew():.2f}") 


    """Answer Q3: WHO correlation matrix + one confounder discussion
    """
    # Correlations with life expectancy
    corrs = df.select_dtypes('number').corr()['life_expectancy'].drop('life_expectancy')
    top_pos = corrs.nlargest(3)
    top_neg = corrs.nsmallest(3)
    print('Top POSITIVE:')
    print(top_pos.round(3))
    print('Top NEGATIVE:')
    print(top_neg.round(3))
    # adult_mortality -0.696
    # hiv/aids -0.564
    # thinness_5-9_yrs -0.460
import pandas as pd
import numpy as np
import os
from statistics_calc import get_df_stats, get_column_stats
import logging
import matplotlib.pyplot as plt
#import seaborn as sns
from scipy import stats
import pingouin as pg



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

def q3(df: pd.DataFrame, log: logging.Logger)-> None:
    """Answer Q3: WHO correlation matrix + one confounder discussion
    Top POSITIVE:
    schooling                          0.716
    income_composition_of_resources    0.694
    bmi                                0.560

    Top NEGATIVE:
    adult_mortality        -0.696
    hiv/aids               -0.557
    thinness_10-19_years   -0.473

    Pearson Correlation between schooling & life_expectancy: 0.716
    Spearman Correlation between schooling & life_expectancy: 0.780

    The partial correlation after controlling GDP is:             n      r         CI95      p_val
                                                        pearson  2938  0.651  [0.63, 0.67]    0.0
    
    Analysis:
    Based on the numeric analysis computed from the correlation matrix,
    the three variables with the highest positive linear relationship to life_expectancy are:
    schooling (Correlation: 0.716)
    income_composition_of_resources (Correlation: 0.694)
    bmi (Correlation: 0.560)

    Top Negative CorrelationsThese variables move in the opposite direction of life expectancy. 
    As these values increase, life expectancy drops:
    adult_mortality (-0.696): The strongest overall factor. High death rates among adults aged 15 to 60 
    directly drop a nation's average lifespan calculation.
    hiv/aids (-0.557): A strong negative driver. High rates of deaths from HIV/AIDS heavily lower life 
    expectancy, especially across developing regions in the historical dataset.
    thinness_10-19_years (-0.473): Shows a clear link between childhood/adolescent malnutrition and lower 
    overall country lifespans.

    Pearson Correlation between schooling & life_expectancy: 0.716
    Spearman Correlation between schooling & life_expectancy: 0.780

    Because the Spearman score is notably higher than the Pearson score, the relationship between 
    schooling and life expectancy is curved (non-linear) or contains outliers. The two metrics move up 
    together reliably, but not in a perfectly straight line.

    GDP is NOT a full confounder: Your original Pearson correlation between schooling and life expectancy 
    was 0.716. After controlling for GDP, the partial correlation (r) drops slightly to 0.651. 
    Because it did not drop sharply toward 0, it proves that schooling has a strong, independent relationship 
    with life expectancy that national wealth alone cannot explain.
    Confidence Interval (CI95 = [0.63, 0.67]): You can be 95% confident that the true background correlation 
    always sits between 0.63 and 0.67.Significance Level (p_val = 0.0): A value of 0.0 means the 
    probability of this relationship happening by pure chance is practically zero, rendering the independent 
    impact of education highly statistically significant.
    """
    log.info(f"################ Q3 answering:") 
    # Correlations with life expectancy
    corrs = df.select_dtypes('number').corr()['life_expectancy'].drop('life_expectancy')
    top_pos = corrs.nlargest(3)
    top_neg = corrs.nsmallest(3)
    log.info('Top POSITIVE:')
    print(top_pos.round(3))
    log.info('Top NEGATIVE:')
    print(top_neg.round(3))

    pearson_corr = df['schooling'].corr(df['life_expectancy'], method='pearson')
    spearman_corr = df['schooling'].corr(df['life_expectancy'], method='spearman')

    log.info(f"Pearson Correlation between schooling & life_expectancy: {pearson_corr:.3f}")
    log.info(f"Spearman Correlation between schooling & life_expectancy: {spearman_corr:.3f}")

    partial_corr = pg.partial_corr(data=df, x='schooling', y='life_expectancy', covar='gdp')
    print(f"The partial correlation after controlling GDP is: {partial_corr.round(3)}")

def q4(df: pd.DataFrame, log: logging.Logger)-> None:
    """
    Answering Q4: Chi-squared test — rating group vs win rate, with effect size
    === Chi-Squared Test Results ===
    Chi-squared Statistic: 278.674
    p-value:               0.000000
    Degrees of Freedom:    4
    Cramér's V (Effect):   0.083

    A p-value of 0.000000 means the probability that this pattern happened by pure random chance is zero. 
    The relationship is highly statistically significant. You can confidently state that a player's rating 
    group does change their probability of winning.
    Cramér's V tells you how much it actually matters in the real world.Any value below 0.10 is considered a 
    negligible or very weak effect.The Reason: Because the dataset has thousands of rows, the Chi-squared 
    test becomes so sensitive that it flags tiny, minor differences as "highly significant." 
    Cramér's V corrects for this sample-size bias and reveals that grouping players by raw rating 
    alone doesn't strongly predict the game's outcome.
    Your metrics prove a highly statistically significant but practically negligible relationship, 
    showing that while absolute rating groups mathematically affect win rates, their real-world predictive 
    impact is incredibly weak.
    """
    log.info(f"################ Q4 answering:") 
    import numpy as np
    import pandas as pd
    from scipy import stats

    df['rating_group'] = pd.qcut(df['white_rating'], q=3, labels=['Low', 'Medium', 'High'])
    contingency_table = pd.crosstab(df['rating_group'], df['winner'])
    chi2, p_val, dof, expected = stats.chi2_contingency(contingency_table)
    n = contingency_table.sum().sum() 
    min_dim = min(contingency_table.shape) - 1  
    cramers_v = np.sqrt(chi2 / (n * min_dim))

    print("=== Chi-Squared Test Results ===")
    print(f"Chi-squared Statistic: {chi2:.3f}")
    print(f"p-value:               {p_val:.6f}")
    print(f"Degrees of Freedom:    {dof}")
    print(f"Cramér's V (Effect):   {cramers_v:.3f}")

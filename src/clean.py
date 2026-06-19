import pandas as pd
import numpy as np
import logging

def clean_chess(df: pd.DataFrame) -> pd.DataFrame: 
    """Cleans the chess games dataset, extracts new features, and validates data quality.
    Args:
        df: A pandas DataFrame containing raw chess game records.

    Returns:
        A cleaned and engineered pandas DataFrame.

    Raises:
        AssertionError: If 'rating_diff' contains null values or if 
            duplicate rows are detected in the dataset.
    """
    df[['time_base', 'time_inc']] = df['time_increment'].str.split('+', expand=True).astype(int)
    df['rating_diff'] = df['white_rating'] - df['black_rating']
    df['opening_family'] = df['opening_fullname'].str.split(':').str[0].str.strip()
    df = df.drop(columns=['opening_response'])  # 93.98% null
    df = df.drop(columns=['opening_variation']) 
    df['is_suspicious'] = df['turns'] < 5  # 342 games
    assert df['rating_diff'].notna().all(), "Data Quality Error: The rating_diff column contains missing values!"
    dup_count = df.duplicated().sum()
    assert dup_count == 0, f"Data Quality Error: Found {dup_count} completely duplicate rows in the dataset!"

    return df

def who_lowering_and_remove_spaces(df: pd.DataFrame)->pd.DataFrame:
    """Reformatting the data by changing everything to lowercase and 
    replacing multiple spaces with an underscore
    """
    orig_cols = list(df.columns)
    new_cols = []
    for col in orig_cols:
        new_cols.append(col.strip().replace('  ', ' ').replace(' ', '_').lower())
    df.columns = new_cols
    return df

def who_rename_columns(df: pd.DataFrame)->pd.DataFrame:
    """Renaming the columns of a datafraem
    """
    df.rename(columns={'thinness_1-19_years':'thinness_10-19_years'}, inplace=True)
    return df

def who_remove_nulls_5th_percentile(df: pd.DataFrame)->pd.DataFrame:
    """
    computing 5th percentile and replacing null values with 0
    """
    mort_5_percentile = np.percentile(df.adult_mortality.dropna(), 5)
    df.adult_mortality = df.apply(lambda x: np.nan if x.adult_mortality < mort_5_percentile else x.adult_mortality, axis=1)
    df.infant_deaths = df.infant_deaths.replace(0, np.nan)
    df.bmi = df.apply(lambda x: np.nan if (x.bmi < 10 or x.bmi > 50) else x.bmi, axis=1)
    df['under-five_deaths'] = df['under-five_deaths'].replace(0, np.nan)
    return df

def who_remove_col(df: pd.DataFrame)->pd.DataFrame:
    """Remoing BMI columns ro eliminate null values
    """
    df.drop(columns='bmi', inplace=True)
    return df

def who_add_yearwise_means(df: pd.DataFrame)->pd.DataFrame:
    """Adding the yearwise means to the data frame
    """
    imputed_data = []
    for year in list(df.year.unique()):
        year_data = df[df.year == year].copy()
        for col in list(year_data.columns)[3:]:
            year_data[col] = year_data[col].fillna(year_data[col].dropna().mean()).copy()
        imputed_data.append(year_data)
    df = pd.concat(imputed_data).copy()
    return df

def who_clean(df: pd.DataFrame)->pd.DataFrame:
    """This function cleans the who dataset dataframes and reutuns a cleaned dataframe
    """
    cleaned_df = df.pipe(
        who_lowering_and_remove_spaces).pipe(
            who_rename_columns).pipe(
                lambda x: x #who_remove_nulls_5th_percentile
                ).pipe(
                  lambda x: x #who_remove_col
                  ).pipe(who_add_yearwise_means)
    return cleaned_df

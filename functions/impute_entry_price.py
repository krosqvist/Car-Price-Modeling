import pandas as pd
import numpy as np

def impute_entry_prices(df):
    df = df.copy()

    # group means
    genmodel_means = df.groupby('Genmodel_ID')['Entry_price'].transform(
    lambda x: np.ceil(x.mean() / 1000) * 1000 if len(x) >= 3 else None)
    year_means = df.groupby('Reg_year')['Entry_price'].transform(
    lambda x: np.ceil(x.mean() / 1000) * 1000 if len(x) >= 10 else None)
    maker_means = df.groupby('Maker')['Entry_price'].transform(
    lambda x: np.ceil(x.mean() / 1000) * 1000 if len(x) >= 100 else None)

    # hierarchical imputation
    df['Entry_price'] = df['Entry_price'].fillna(genmodel_means)
    df['Entry_price'] = df['Entry_price'].fillna(year_means)
    df['Entry_price'] = df['Entry_price'].fillna(maker_means)

    # drop remaining missing
    df = df.dropna(subset=['Entry_price'])

    return df
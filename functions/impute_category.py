import numpy as np
import pandas as pd

def impute_car_features(df):
    df = df.copy()

    target_columns = ['Bodytype', 'Engin_size']

    for col in target_columns:
        if col == 'Engin_size':
            mask = df['Fuel_type'].str.lower() != 'electric'
            target = df.loc[mask, col]
            agg_func = lambda x: np.nanmean(x) if len(x) >= 3 else np.nan
        elif df[col].dtype.kind in 'biufc':  # numeric columns
            mask = df.index
            target = df[col]
            agg_func = lambda x: np.nanmean(x) if len(x) >= 3 else np.nan
        else:  # categorical columns
            mask = df.index
            target = df[col]
            def safe_mode(x):
                m = x.mode()
                return m.iloc[0] if len(m) else np.nan
            agg_func = lambda x: safe_mode(x) if len(x) >= 3 else np.nan

        genmodel_vals = df.groupby('Genmodel_ID')[col].transform(agg_func)
        year_vals = df.groupby('Reg_year')[col].transform(agg_func)
        maker_vals = df.groupby('Maker')[col].transform(agg_func)

        df.loc[mask, col] = target.fillna(genmodel_vals).fillna(year_vals).fillna(maker_vals)

    return df

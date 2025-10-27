import pandas as pd
import numpy as np

def robust_numerical_imputer(df, features_to_impute, min_group_size=4):
    df = df.copy()
    
    group_features = ['Engin_size','Maker','Genmodel','Reg_year','Gearbox','Fuel_type','Bodytype']
    
    drop_order = ['Gearbox','Bodytype','Fuel_type','Engin_size','Reg_year','Genmodel','Maker']
    
    # the process is repeated for each feature that needs to be imputed.
    for feat in features_to_impute:
        missing_mask = df[feat].isna()

        # ignore errors
        if missing_mask.sum() == 0:
            continue  
        
        # the process is repeated at different levels of specificity for the grouping
        for n_drop in range(len(drop_order)+1):
            # grab the features used for grouping
            active_groups = [f for f in group_features if f not in drop_order[:n_drop] and f != feat]

            # skip if the drop_order list has been exhausted
            if len(active_groups) == 0:
                break

            # grouping and ensuring group size is sufficient
            group_sizes = df.groupby(active_groups)[feat].transform('count')
            valid_group = group_sizes >= min_group_size
            
            # calculate the mean for valid groups
            group_mean = df[valid_group].groupby(active_groups)[feat].mean().reset_index()

            df = df.merge(group_mean, on=active_groups, how='left', suffixes=('', '_mean'))
            
            # fill with the calculated means
            fill_mask = df[feat].isna() & df[feat+'_mean'].notna()
            df.loc[fill_mask, feat] = df.loc[fill_mask, feat+'_mean']

            df = df.drop(columns=[feat+'_mean'])
            
            # quit if the imputing could be completed with the current specificity level
            if df[feat].notna().all():
                break
        

    # dropping rows with missing numerical features
    df = df.dropna(subset=features_to_impute)
    
    return df
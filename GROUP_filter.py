import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, 'data', 'Ad_table.csv')

import pandas as pd
pd.set_option('display.max_rows', None, 'display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_colwidth', None)

df = pd.read_csv(data_path, low_memory=False)

df = df.apply(lambda col: col.map(lambda x: x.lower() if isinstance(x, str) else x))

# Numeroiksi
df['Reg_year'] = pd.to_numeric(df['Reg_year'], errors='coerce')
df['Adv_year'] = pd.to_numeric(df['Adv_year'], errors='coerce')
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
df['Runned_Miles'] = pd.to_numeric(df['Runned_Miles'], errors='coerce')


df = df.dropna(subset=['Price', 'Reg_year', 'Adv_year', 'Maker', 'Genmodel', "Runned_Miles"])


# https://www.macrotrends.net/global-metrics/countries/gbr/united-kingdom/inflation-rate-cpi

inflation_index = {
    2025: 1.0000,
    2024: 1.0327,
    2023: 1.1028,
    2022: 1.1902,
    2021: 1.2202,
    2020: 1.2322,
    2019: 1.2537,
    2018: 1.2824,
    2017: 1.3152,
    2016: 1.3285,
    2015: 1.3334,
    2014: 1.3527,
    2013: 1.3837,
    2012: 1.4193,
    2011: 1.4741,
    2010: 1.5108,
    2009: 1.5404,
    2008: 1.5946,
    2007: 1.6327,
    2006: 1.6729,
    2005: 1.7078,
    2004: 1.7316,
    2003: 1.7555,
    2002: 1.7822,
    2001: 1.8094,
    2000: 1.8308,
    1999: 1.8628,
    1998: 1.8967,
    1997: 1.9385,
    1996: 1.9937,
    1995: 2.0475
}

new_prices = []
for _, row in df.iterrows():
    new_prices.append(row["Price"]*inflation_index[row["Adv_year"]])
df["Price"]=new_prices

df['Inflation_index'] = df['Adv_year'].map(inflation_index)


#################################################################################
# Pyöristyksiä ryhmittelyä varten
def year_bucket(year):
    return (year // 4) * 4  

df['Adv_year_bucket'] = df['Adv_year'].apply(year_bucket)
df['Reg_year_bucket'] = df['Reg_year'].apply(year_bucket)

df['km'] = (df['Runned_Miles']*1.60934 // 20000) * 20000


##################################################################################
# Muutoksia dataan
# Moottorikoko numeroksi
df['Engin_size'] = df['Engin_size'].str.replace('l', '', case=False, regex=False).astype(float)

# Ikä erikseen
df['Vehicle_age'] = df['Adv_year'] - df['Reg_year']

# Pois superautot, hajoitetut (tmv) ja paljon ajetut autot
df = df[df['Price']<=80000]
df = df[df['Price']>=500]
df = df[df["Runned_Miles"]*1.60934<=300000]

# Add original/entry price to table
data_path = os.path.join(base_dir, 'data', 'Price_table.csv')
price_table = pd.read_csv(data_path)
price_data = price_table[['Genmodel_ID', 'Year', 'Entry_price']]
df = df.merge(price_data,
               left_on=['Genmodel_ID', 'Reg_year'],
                  right_on=['Genmodel_ID', 'Year'],
                  how='left')

df['Inflation_index_entry'] = df['Year'].map(inflation_index)



# Imputing missing values
from functions.impute_entry_price import impute_entry_prices
from functions.impute_category import impute_car_features
df=impute_entry_prices(df)
df=impute_car_features(df)


#################################################################################
# Ryhmittely ominaisuuksien mukaan
grouped = df.groupby(['Genmodel', 'Adv_year_bucket', 'Reg_year_bucket', 'km'])

# 
filtered = grouped.filter(lambda x: len(x) >= 28).drop(labels=['Adv_ID',
                                                               'Adv_month',
                                                               'Seat_num',
                                                                'Door_num',
                                                                'km', 
                                                                'Adv_year_bucket', 
                                                                'Reg_year_bucket',
                                                                ], axis=1)


missing = filtered.isna().sum()
print(f"Count of missing values\n{missing[missing > 0]}\nDataframe size: {filtered.shape}")
#print(f'sub 20000 priced {filtered[filtered['Price']<20000].count()}')

# The new file is saved to the "data" folder.
output_path = os.path.join(base_dir, 'data', 'grouped_cars.csv')
filtered.to_csv(output_path, index=False)


import pandas as pd
pd.set_option('display.max_rows', None, 'display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_colwidth', None)

df = pd.read_csv("Ad_table.csv", low_memory=False)

# Numeroiksi
df['Reg_year'] = pd.to_numeric(df['Reg_year'], errors='coerce')
df['Adv_year'] = pd.to_numeric(df['Adv_year'], errors='coerce')
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
df['Runned_Miles'] = pd.to_numeric(df['Runned_Miles'], errors='coerce')
# Tyhjät pois (pitää testata lisää jos kiinnostaa)
df = df.dropna(subset=['Price', 'Reg_year', 'Adv_year', 'Maker', 'Genmodel', 'Color', "Runned_Miles"])


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


df['Inflation_index'] = df['Adv_year'].map(inflation_index)


'''
# TÄYTYY LISÄTÄ INFLAATIO KORJAUS. MAHDOLLISESTI MYÖS YLEINEN MARKKINOIDEN KEHITYS(?)
def adjust_for_inflation(row):
    year = row["Adv_year"]
    price = row["Price"]
    return round(price * inflation_index[year])

# Create new column
df["Price_inflation_adj"] = df.apply(adjust_for_inflation, axis=1)
'''


# Pois superautot, 
df = df[df['Price']<=50000]
df = df[df["Runned_Miles"]*1.60934<=300000]

def year_bucket(year):
    return (year // 3) * 3  

df['Adv_year_bucket'] = df['Adv_year'].apply(year_bucket)
df['Reg_year_bucket'] = df['Reg_year'].apply(year_bucket)



# Moottorikoko numeroksi
df['Engin_size'] = df['Engin_size'].str.replace('L', '', regex=False).astype(float)

# Kilometreiksi ja pyöristys (44554km // 10000=4...)
df['km'] = (df['Runned_Miles']*1.60934 // 10000) * 10000

# Ikä erikseen
df['Vehicle_age'] = df['Adv_year'] - df['Reg_year']



# Add original price to table
price_table = pd.read_csv('Price_table.csv')
price_data = price_table[['Genmodel_ID', 'Year', 'Entry_price']]
df = df.merge(price_data,
               left_on=['Genmodel_ID', 'Reg_year'],
                  right_on=['Genmodel_ID', 'Year'],
                  how='left')




# Ryhmittely ominaisuuksien mukaan (vuosi on todella tiukka ehto)
grouped = df.groupby(['Genmodel_ID', 'Adv_year_bucket', 'Reg_year_bucket', 'km'])

# 
filtered = grouped.filter(lambda x: len(x) >= 50).drop(labels=['Adv_ID',
                                                               'Adv_month',
                                                               'Seat_num',
                                                                'Door_num',
                                                                'Runned_Miles'
                                                                ], axis=1)

#accepted_models = ["34_2"]
#filtered = filtered[filtered['Genmodel_ID'].isin(accepted_models)]

filtered.to_csv("grouped_cars.csv", index=False)

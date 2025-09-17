import pandas as pd
pd.set_option('display.max_rows', None, 'display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_colwidth', None)

df = pd.read_csv("Ad_table.csv")

# Numeroiksi
df['Reg_year'] = pd.to_numeric(df['Reg_year'], errors='coerce')
df['Adv_year'] = pd.to_numeric(df['Adv_year'], errors='coerce')
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
df['Runned_Miles'] = pd.to_numeric(df['Runned_Miles'], errors='coerce')
# Tyhjät pois (pitää testata lisää jos kiinnostaa)
df = df.dropna(subset=['Price', 'Reg_year', 'Adv_year', 'Maker', 'Genmodel', 'Color', "Runned_Miles"])


def year_bucket(year):
    return (year // 3) * 3  # groups into 3-year bins, e.g. 2016-2018, 2019-2021

df['Adv_year_bucket'] = df['Adv_year'].apply(year_bucket)
df['Reg_year_bucket'] = df['Reg_year'].apply(year_bucket)

# Pois superautot yms.
df = df[df['Price']<=50000]


# Kilometreiksi ja pyöristys (44554km // 10000=4...)
df['km'] = (df['Runned_Miles']*1.60934 // 10000) * 10000

# Ryhmittely ominaisuuksien mukaan (vuosi on todella tiukka ehto)
grouped = df.groupby(['Genmodel_ID', 'Adv_year_bucket', 'Reg_year_bucket', 'km'])

# 
filtered = grouped.filter(lambda x: len(x) >= 30).drop(labels=['Adv_ID',
                                                               'Adv_month',
                                                               'Seat_num',
                                                                'Door_num',
                                                                'Runned_Miles'
                                                                ], axis=1)

#accepted_models = ["34_2"]
#filtered = filtered[filtered['Genmodel_ID'].isin(accepted_models)]
print(filtered)
filtered.to_csv("grouped_cars.csv", index=False)


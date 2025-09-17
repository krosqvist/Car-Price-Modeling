import pandas as pd

df = pd.read_csv("Ad_table.csv")

# Numeroiksi
df['Reg_year'] = pd.to_numeric(df['Reg_year'], errors='coerce')
df['Adv_year'] = pd.to_numeric(df['Adv_year'], errors='coerce')
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
df['Runned_Miles'] = pd.to_numeric(df['Runned_Miles'], errors='coerce')
# Tyhjät pois (pitää testata lisää jos kiinnostaa)
df = df.dropna(subset=['Price', 'Reg_year', 'Adv_year', 'Maker', 'Genmodel', 'Color', "Runned_Miles"])

# Pois superautot yms.
df = df[df['Price']<=50000]


# Kilometreiksi ja pyöristys (44554km // 10000=4...)
df['km'] = (df['Runned_Miles']*1.60934 // 10000) * 10000

# Ryhmittely ominaisuuksien mukaan (vuosi on todella tiukka ehto)
grouped = df.groupby(['Genmodel_ID', 'Adv_year', 'Reg_year', 'km'])

# 
filtered = grouped.filter(lambda x: len(x) >= 30).drop(labels=['Adv_ID',
                                                               'Adv_month',
                                                               'Seat_num',
                                                                'Door_num',
                                                                'Runned_Miles'
                                                                ], axis=1)


print(filtered.shape)
filtered.to_csv("grouped_cars.csv", index=False)


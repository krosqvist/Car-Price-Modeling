import pandas as pd


df = pd.read_csv('data/Ad_table.csv', low_memory=False)

# Lower text on rows (the website inputs are also lowered)
df = df.apply(lambda col: col.map(lambda x: x.lower() if isinstance(x, str) else x))

# Some features are changed to numeric values for processing
df['Reg_year'] = pd.to_numeric(df['Reg_year'], errors='coerce')
df['Adv_year'] = pd.to_numeric(df['Adv_year'], errors='coerce')
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
df['Runned_Miles'] = pd.to_numeric(df['Runned_Miles'], errors='coerce')


df = df.dropna(subset=['Price', 'Reg_year', 'Adv_year', 'Maker', 'Genmodel', "Runned_Miles"])


#################################################################################
# Rounding years and runned miles for grouping
def year_bucket(year):
    return (year // 4) * 4  

df['Adv_year_bucket'] = df['Adv_year'].apply(year_bucket)
df['Reg_year_bucket'] = df['Reg_year'].apply(year_bucket)

# kilometers used temporarily (due to familiriality)
df['km'] = (df['Runned_Miles']*1.60934 // 20000) * 20000

#################################################################################
# Group by mandatory features
grouped = df.groupby(['Genmodel', 'Adv_year_bucket', 'Reg_year_bucket', 'km'])

# Filter groups with too few elements/rows
# Remove unnecessary columns
filtered = grouped.filter(lambda x: len(x) >= 28).drop(labels=['Adv_ID',
                                                               'Adv_month',
                                                               'Seat_num',
                                                                'Door_num',
                                                                'km', 
                                                                'Adv_year_bucket', 
                                                                'Reg_year_bucket',
                                                                'Color'
                                                                ], axis=1)
df = filtered


##################################################################################
# Additional changes

# The engine size is changed to a numerical form
df['Engin_size'] = df['Engin_size'].str.replace('l', '', case=False, regex=False).astype(float)

# Vehicle age is used as a numerical feature in training
df['Vehicle_age'] = df['Adv_year'] - df['Reg_year']
df.drop(labels=['Adv_year'],axis=1)

# Remove extreme cases and fully electric vehicles from the data
df = df[df['Price']<=80000]
df = df[df['Price']>=500]
df = df[df["Runned_Miles"]*1.60934<=300000]
df = df[df['Fuel_type']!='electric']

# Add original/entry price to table
price_table = pd.read_csv('data/Price_table.csv')
price_data = price_table[['Genmodel_ID', 'Year', 'Entry_price']]
df = df.merge(price_data,
               left_on=['Genmodel_ID', 'Reg_year'],
                  right_on=['Genmodel_ID', 'Year'],
                  how='left')


# Imputing missing values
from functions.impute_numerical import robust_numerical_imputer
from functions.impute_category import robust_category_imputer
categoricals_to_impute = ['Engin_size', 'Gearbox', 'Fuel_type', 'Bodytype']
numericals_to_impute = ['Entry_price']
df=robust_category_imputer(df, categoricals_to_impute)
df=robust_numerical_imputer(df, numericals_to_impute)

##############################################################################################################


# missing = filtered.isna().sum()
# print(f"Count of missing values\n{missing[missing > 0]}\nDataframe size: {filtered.shape}")


# The new file is saved to the "data" folder.
df.to_csv('data/grouped_cars.csv', index=False)


import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
base_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(base_dir)
data_path = os.path.join(parent_dir, 'data', 'Ad_table.csv')
data_path2 = os.path.join(parent_dir, 'data', 'Price_table.csv')



import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Set the limits for how many rows pandas shows in terminal
pd.set_option('display.max_rows', 100, 'display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_colwidth', None)

# Read all the required data from the database
ad_table = pd.read_csv(data_path, low_memory=False)
price_table = pd.read_csv(data_path2)
price_data = price_table[['Genmodel_ID', 'Year', 'Entry_price']]

data = ad_table[['Maker', 'Genmodel', 'Genmodel_ID', 'Adv_year', 'Reg_year', 'Runned_Miles', 'Engin_size', 'Price']]

# Merge tables to form one array with required data
data = data.merge(price_data,
                  left_on=['Genmodel_ID', 'Reg_year'],
                  right_on=['Genmodel_ID', 'Year'],
                  how='left')

# Choose the parameters for plotting
data = data.dropna(subset=['Entry_price'])
data['Price'] = pd.to_numeric(data['Price'], errors='coerce')
data['Entry_price'] = pd.to_numeric(data['Entry_price'], errors='coerce')
data['Price_percentage'] = data['Price'] / data['Entry_price'] * 100

# Here pick which car to plot
# If wanted a whole manufacturer eg. toyota choose 'Maker' instead of 'Genmodel_ID'
accepted_models = ["29_13"]
data = data[data['Genmodel_ID'].isin(accepted_models)]


# Extra filtering if needed
#data = data[data['Reg_year'] == 2014]
data = data[(data['Reg_year'] >= 2001) & (data['Reg_year'] <= 2007)]



print(data)

x = pd.to_numeric(data['Runned_Miles'], errors='coerce')
y = pd.to_numeric(data['Price_percentage'], errors='coerce')

# Plotting settings
plt.figure(figsize=(8,6))
plt.scatter(x, y, alpha=0.5)  # alpha for transparency
plt.xlabel("Runned Miles")
plt.ylabel("Selling Price Compared to Original Price (%)")
plt.title("Price vs Runned Miles")
#plt.xlim(0,200000)
plt.ylim(0,100)
plt.grid(True)
plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=6))  # about 6 ticks
plt.gca().yaxis.set_major_locator(MaxNLocator(nbins=6))
plt.show()
plt.savefig("analysis_files/analysis_plot.png")

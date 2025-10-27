import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
base_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(base_dir)
data_path = os.path.join(parent_dir, 'data', 'Ad_table.csv')
data_path2 = os.path.join(parent_dir, 'data', 'Price_table.csv')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

models = pd.read_csv(data_path2)
models = models.drop("Genmodel_ID", axis=1).dropna()
cars = pd.read_csv(data_path, low_memory=False)
cars = cars[["Maker", "Genmodel", "Reg_year", "Price", "Runned_Miles", "Adv_year"]].dropna()
#cars = cars[cars["Maker"] == "Ford"]
#cars = cars[cars["Genmodel"] == "Ka"]
#cars = cars[cars["Reg_year"] < 2008]
models_dict = {}
for _, row in models.iterrows():
    models_dict[(row["Maker"], row["Genmodel"], row["Year"])] = int(row["Entry_price"])
price_percent = []
miles = []
age = []
for _, row in cars.iterrows():
    if (row["Maker"], row["Genmodel"], row["Reg_year"]) in models_dict:
        try:
            x = (int(row["Price"]), int(row["Runned_Miles"]))
            price_percent.append(int(row["Price"]) / models_dict[(row["Maker"], row["Genmodel"], row["Reg_year"])])
            miles.append(int(row["Runned_Miles"]))
            age.append(int(row["Adv_year"])-int(row["Reg_year"]))
        except:
            pass
plt.plot(age, price_percent, 'o', alpha=0.01)
plt.xlim(0, 20)
plt.ylim(0, 1.2)
plt.savefig('analysis_files/comparison_plot.png', dpi=300, bbox_inches='tight')
    
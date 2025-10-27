import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
data_path = os.path.join(base_dir, 'data', 'Ad_table.csv')
data_path2 = os.path.join(base_dir, 'data', 'Price_table.csv')
#################################################################################
#imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as sns
import math
from sklearn.metrics import mean_squared_error
import joblib

#################################################################################

models = pd.read_csv(data_path2)
models = models.drop("Genmodel_ID", axis=1).dropna()
cars = pd.read_csv(data_path, low_memory=False)
cars = cars[["Maker", "Genmodel", "Adv_year", "Adv_month", "Color", "Reg_year", "Runned_Miles", "Price"]].dropna()
models_dict = {}
for _, row in models.iterrows():
    models_dict[(row["Maker"], row["Genmodel"], row["Year"])] = int(row["Entry_price"])

# goal
price = []

# parameters
colors = {}
colorset = set(cars["Color"])
for i in colorset:
    colors[i] = []
    makers = {}
makerset = set(cars["Maker"])
for i in makerset:
    makers[i] = []
new_prices = []
age = []
runned_miles = []
adv_year = []
summer = []


for _, row in cars.iterrows():
    if (row["Maker"], row["Genmodel"], row["Reg_year"]) in models_dict:
        try:
            # test
            t=int(row["Price"])
            t=int(row["Adv_year"])
            t=int(row["Adv_month"])
            t=int(row["Reg_year"])
            t=int(row["Runned_Miles"])
            t=math.log(int(row["Adv_year"])-int(row["Reg_year"]))
            if int(row["Price"])>200000:
                continue
            if int(row["Runned_Miles"])>300000:
                continue

            # goal
            price.append(int(row["Price"]))

            # variables
            for i in colors:
                if row["Color"] == i:
                    colors[i].append(1)
                else:
                    colors[i].append(0)
            for i in makers:
                if row["Maker"] == i:
                    makers[i].append(1)
                else:
                    makers[i].append(0)
            if 4 < int(row["Adv_month"]) and int(row["Adv_month"]) < 11:
                summer.append(1)
            else:
                summer.append(0) 
            new_prices.append(int(models_dict[(row["Maker"], row["Genmodel"], row["Reg_year"])]))
            age.append(math.log(int(row["Adv_year"])+int(row["Adv_month"])/12-int(row["Reg_year"])))
            runned_miles.append(int(row["Runned_Miles"])/(int(row["Adv_year"])+int(row["Adv_month"])/12-int(row["Reg_year"])))
            adv_year.append(int(row["Adv_year"]))

        except:
            pass

#costruct y
y = pd.DataFrame(np.array([price]).T, columns=["price"])

#construct x
thedict = {"adv_year": adv_year, "runned_miles": runned_miles, "age": age, "new_prices": new_prices, "summer": summer}
thedict = thedict | makers | colors
x= pd.DataFrame(data=thedict)

print(x.columns.tolist())

#linear regression
reg = LinearRegression().fit(x, y)
print(reg.score(x, y))
print(mean_squared_error(y, reg.predict(x)))
print(math.sqrt(mean_squared_error(y, reg.predict(x))))
print(reg.coef_)

sns.regplot(x=x["summer"], y=y["price"], scatter_kws={"alpha": 0.01})
sns.regplot(x=x["summer"], y=y["price"], marker="None", color="red")
plt.show()
plt.savefig("analysis_files/LINEAR_model_result.png")
joblib.dump(reg, 'car_price_model.pkl')
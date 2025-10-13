import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
from functions.market_trend_generalizator import market_trend_generalizator
import matplotlib.pyplot as plt

data_path = os.path.join(base_dir, 'data', 'grouped_cars.csv')
df = pd.read_csv(data_path)

trend = market_trend_generalizator(df=df, start_year=2012, end_year=2021, top_n=200)
print("Trend shape:", trend.shape)
print(trend.head())
plt.figure(figsize=(9,5))
plt.plot(trend["Adv_year"], trend["mean"], marker='o')
plt.fill_between(trend["Adv_year"],
                 trend["mean"] - trend["std"],
                 trend["mean"] + trend["std"],
                 alpha=0.2)
plt.xlabel("Advertised Year")
plt.ylabel("Average Price (% of Entry Price, real terms)")
plt.title("Market-Level Resale Value Trend (Inflation-Adjusted)")
plt.grid(True, alpha=0.3)
plt.show()
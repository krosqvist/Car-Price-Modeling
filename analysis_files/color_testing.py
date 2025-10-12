import numpy as np
import pandas as pd

df = pd.read_csv("grouped_cars.csv")

# unique_colors
# =df['Color'].unique()
# print(unique_cols)

X = 3000
count_col = df['Color'].value_counts()
common_col = count_col[count_col >= X].index
df = df[df['Color'].isin(common_col)]

color_effects = []

for model_id, subdf in df.groupby('Genmodel_ID'):
    if len(subdf) > 100:
        group_mean = subdf['Price'].mean()
        color_price_diff = subdf.groupby('Color')['Price'].mean() - group_mean
        color_effects.append(color_price_diff)


effect = pd.concat(color_effects, axis=1).T.fillna(0)

mean_color_effect = effect.mean().sort_values(ascending=False)

print("Average price effect by color (controlled for model, year, mileage):")
print(mean_color_effect)

mean_color_effect.to_csv("color_price_effect.csv", header=['Avg_Price_Effect'])
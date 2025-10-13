import pandas as pd
# Used to check which options to give in the boxes

df = pd.read_csv("grouped_cars.csv")

print("Makers:", df["Maker"].unique())
print("Models:", df["Genmodel"].unique())
print("Bodytypes:", df["Bodytype"].unique())
print("Gearboxes:", df["Gearbox"].unique())
print("Fuel types:", df["Fuel_type"].unique())


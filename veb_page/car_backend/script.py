import sys
import pandas as pd
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import joblib

args = sys.argv

load_dotenv()
MONGODB_URI = os.getenv('MONGODB_URI')

client = MongoClient(MONGODB_URI)
db = client['CarData']
collection = db['cars']

model = joblib.load('car_price_model.pkl')

new_data = pd.DataFrame([{
    'Maker': args[1],
    'Genmodel': args[2],
    'Gearbox': args[3],
    'Fuel_type': args[4],
    'Bodytype': args[5],
    'Engin_size': float(args[6]),
    'Reg_year': int(args[7]),
    'km': int(args[8]),
    'Adv_year': 2025
}])

query = {
    "Maker": new_data.loc[0, "Maker"],
    "Genmodel": new_data.loc[0, "Genmodel"],
    "Reg_year": int(new_data.loc[0, "Reg_year"])
}

car_doc = collection.find_one(query, {"Entry_price": 1, "_id": 0})

if car_doc and "Entry_price" in car_doc:
    entry_price = car_doc["Entry_price"]
    new_data["Entry_price"] = entry_price
else:
    new_data["Entry_price"] = 0 # Makeshift solution

predicted_price = model.predict(new_data)
print(f'\nPredicted price for given car details: {predicted_price[0]:.0f} £ or {predicted_price[0]*1.15:.0f} €.')
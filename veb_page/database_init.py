import os
from dotenv import load_dotenv
import pandas as pd
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["CarData"]
collection = db["cars"]

df = pd.read_csv("grouped_cars.csv")

# Convert DataFrame to dicts and insert
collection.drop()
collection.insert_many(df.to_dict(orient="records"))
import sys
import pandas as pd
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import requests
import joblib
from grapher import grapher
import io
import base64
#import tempfile # For local testing

args = sys.argv

load_dotenv()
MONGODB_URI = os.getenv('MONGODB_URI')
MODEL_PATH = '/tmp/car_price_model.pkl'

# For local testing
'''MODEL_PATH = os.path.join(tempfile.gettempdir(), "car_price_model.pkl")
if os.path.exists(MODEL_PATH):
    os.remove(MODEL_PATH)'''

MODEL_URL = os.getenv('LINEAR_MODEL_URL')

client = MongoClient(MONGODB_URI)
db = client['CarData']
collection = db['cars']


def load_model():
    # Check if cached file exists
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            head = f.read(10)
        # If first bytes look like HTML, delete cache
        if head.startswith(b'<'):
            os.remove(MODEL_PATH)

    # Load from cache if valid
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)

    # Download from GitHub Release
    response = requests.get(MODEL_URL)
    response.raise_for_status()
    with open(MODEL_PATH, 'wb') as f:
        f.write(response.content)

    # Verify file
    with open(MODEL_PATH, 'rb') as f:
        head = f.read(10)
        if head.startswith(b'<'):
            raise ValueError('Downloaded file looks like HTML, check MODEL_URL')
    return joblib.load(MODEL_PATH)

new_data = pd.DataFrame([{
    'Maker': args[1].title(),
    'Genmodel': args[2].title(),
    'Gearbox': args[3].title(),
    'Fuel_type': args[4].title(),
    'Bodytype': args[5].title(),
    'Engin_size': float(args[6]),
    'Reg_year': int(args[7]),
    'Runned_Miles': int(args[8]),
    'Adv_year': 2025
}])

query = {
    'Maker': new_data.loc[0, 'Maker'],
    'Genmodel': new_data.loc[0, 'Genmodel'],
    'Reg_year': int(new_data.loc[0, 'Reg_year'])
}

car_doc = collection.find_one(
    query,
    {
        'Entry_price': 1,
        'Inflation_index': 1,
        'Inflation_index_entry': 1,
        '_id': 0
    }
)

if car_doc and 'Entry_price' in car_doc:
    entry_price = car_doc['Entry_price']
    new_data['Entry_price'] = entry_price
    new_data['Inflation_index'] = car_doc['Inflation_index']
    new_data['Inflation_index_entry'] = car_doc['Inflation_index_entry']
    message = ''
else:
    new_data['Entry_price'] = 0 # Makeshift solution
    new_data['Inflation_index'] = 1
    new_data['Inflation_index_entry'] = 1
    message = 'Can not predict price for a car with given details.'

model = load_model()
predicted_price = model.predict(new_data)
if message:
    print(message)
else:
    print(f'\nPredicted price for given car details: {predicted_price[0]:.0f} £ or {predicted_price[0]*1.15:.0f} €.')

grapher(
    model=model,
    maker=new_data.loc[0, 'Maker'],
    genmodel=new_data.loc[0, 'Genmodel'],
    reg_year=new_data.loc[0, 'Reg_year'],
    engin_size=new_data.loc[0, 'Engin_size'],
    gearbox=new_data.loc[0, 'Gearbox'],
    fuel_type=new_data.loc[0, 'Fuel_type'],
    bodytype=new_data.loc[0, 'Bodytype'],
    miles=new_data.loc[0, 'Runned_Miles'],
)
import pandas as pd
import joblib

model = joblib.load('car_price_model.pkl')

new_data = pd.DataFrame([{
    'Maker': 'Audi',
    'Genmodel_ID': '7_3',
    'Gearbox': 'Manual',
    'Fuel_type': 'Diesel',
    'Bodytype': 'Hatchback',
    'Engin_size': 1.6,
    'Vehicle_age': 7,
    'km': 192000, # mittarilukemalla liian iso vaikutus hintaan 100k - 7765, 192k - 4203
    'Entry_price': 20170,
    'Inflation_index': 1295
}])

predicted_price = model.predict(new_data)
print(predicted_price)
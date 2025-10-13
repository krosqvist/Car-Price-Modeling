import pandas as pd
import joblib
from functions.predictor import predict_car_price

model = joblib.load('car_price_model.pkl')
model2 = joblib.load('car_price_model_linear.pkl')

predict_car_price(model = model,
                  maker= 'Volvo',
                  genmodel= 'V40',
                  reg_year= 2019,
                  engin_size= '3',
                  gearbox= 'Manual',
                  fuel_type= 'Petrol',
                  bodytype= 'SUV',
                  miles= '100000',
                  data_path= 'data/grouped_cars.csv',
                  )

predict_car_price(model = model2,
                  maker= 'Volvo',
                  genmodel= 'V40',
                  reg_year= 2019,
                  engin_size= '3',
                  gearbox= 'Manual',
                  fuel_type= 'Petrol',
                  bodytype= 'SUV',
                  miles= '100000',
                  data_path= 'data/grouped_cars.csv',
                  )
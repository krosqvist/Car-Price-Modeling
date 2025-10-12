import pandas as pd
import joblib
from functions.predictor import predict_car_price

model = joblib.load('car_price_model.pkl')

predict_car_price(model = model,
                  maker= 'Volvo',
                  genmodel= 'V40',
                  reg_year= 2019,
                  engin_size= '2',
                  gearbox= 'Manual',
                  fuel_type= 'Petrol',
                  bodytype= 'SUV',
                  miles= '55000',
                  data_path= 'data/grouped_cars.csv',
                  )



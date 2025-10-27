import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import joblib
from functions.predictor import predict_car_price

#########################################################################################

model = joblib.load('RANDF_car_price.pkl')
model2 = joblib.load('LINEAR_car_price.pkl')

# Testing 
# note that the predictor function doesn't lower inputs automatically
print('Estimation transformed target regressor:')
predict_car_price(model = model2,
                  maker= 'volvo',
                  genmodel= 'V40',
                  reg_year= 2019,
                  engin_size= '2',
                  gearbox= 'manual',
                  fuel_type= 'petrol',
                  bodytype= 'suv',
                  miles= '55000',
                  data_path= 'data/grouped_cars.csv',
                  )

predict_car_price(model = model2,
                  maker= 'toyota',
                  genmodel= 'avensis',
                  reg_year= 2012,
                  engin_size= '2',
                  gearbox= 'manual',
                  fuel_type= 'diesel',
                  bodytype= 'saloon',
                  miles= '116000',
                  data_path= 'data/grouped_cars.csv',
                  )



print('\nEstimations with random forest regressor:')
predict_car_price(model = model,
                  maker= 'volvo',
                  genmodel= 'V40',
                  reg_year= 2019,
                  engin_size= '2',
                  gearbox= 'manual',
                  fuel_type= 'petrol',
                  bodytype= 'suv',
                  miles= '55000',
                  data_path= 'data/grouped_cars.csv',
                  )

predict_car_price(model = model,
                  maker= 'toyota',
                  genmodel= 'avensis',
                  reg_year= 2012,
                  engin_size= '2',
                  gearbox= 'manual',
                  fuel_type= 'diesel',
                  bodytype= 'estate',
                  miles= '99000',
                  data_path= 'data/grouped_cars.csv',
                  )
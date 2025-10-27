import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import joblib
import matplotlib.pyplot as plt
from functions.grapher import grapher

#########################################################################################

model = joblib.load('RANDF_car_price.pkl')

# note that the grapher doesn't lower inputs automatically
grapher(model = model,
                  maker= 'volvo',
                  genmodel= 'V40',
                  reg_year= 2019,
                  engin_size= '2',
                  gearbox= 'manual',
                  fuel_type= 'petrol',
                  bodytype= 'suv',
                  miles= '55000',
                  data_path= 'data/grouped_cars.csv',)

plt.savefig("analysis_files/car_price_plot.png")
plt.close()
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from functions.predictor2 import predict_car_price

def grapher(model, maker, genmodel, reg_year, engin_size=None,
                      gearbox=None, fuel_type=None, bodytype=None,
                      miles=None, data_path='data/grouped_cars.csv'):
    if miles == None:
        miles = (2025-reg_year)*7000
    else:
        miles = int(miles)
    x = []
    y = []
    for i in range(2025, 2031):
        x.append(i)
        y.append(predict_car_price(model, maker, genmodel, reg_year, engin_size=engin_size,
                      gearbox=gearbox, fuel_type=fuel_type, bodytype=bodytype,
                      miles=miles+i*7000, data_path='data/grouped_cars.csv', adv_year=i)[0])
    
     # Fit 2nd-degree polynomial
    coeffs = np.polyfit(x, y, deg=2)
    poly = np.poly1d(coeffs)

    # Generate smooth curve for plotting
    x_smooth = np.linspace(2024, 2031, 300)
    y_pred = poly(x_smooth)

    # Confidence interval: ±10% of predicted value
    y_upper = y_pred + 1750
    y_lower = y_pred - 1750

    # Plotting
    plt.figure(figsize=(8, 5))
    plt.plot(x_smooth, y_pred, label='Predicted car price', color='green')
    plt.fill_between(x_smooth, y_lower, y_upper, color='green', alpha=0.2, label='50 % Confidence interval')

    # Dots are intentionally left invisible
    # plt.scatter(x, y, alpha=0)

    plt.ylim(0, y[0]+5000)
    plt.legend()
    plt.xlim(2024.75, 2030.25)
    plt.grid(True)
    plt.show()
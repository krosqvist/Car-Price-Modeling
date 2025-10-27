import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from functions.predictor2 import predict_car_price
from scipy.optimize import curve_fit

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
                      miles=miles+(i-2025)*7000, data_path=data_path, adv_year=i)[0])
        
    def exponential_model(x, a, b):
        return a * np.exp(-b * (x-2025))
    
    x = np.array(x)
    y = np.array(y)

    # Fit exponential model to the data
    try:
        popt, _ = curve_fit(exponential_model, x, y, maxfev=10000)
    except RuntimeError:
        print("Exponential fit failed. Falling back to linear fit.")
        return

    # Generate smooth curve for plotting
    x_smooth = np.linspace(2024, 2031, 300)
    y_pred = exponential_model(x_smooth, *popt)

    # Confidence interval (approximate): ±
    y_upper = y_pred + y_pred * 0.14845856288 * 1.05**(x_smooth-2025)
    y_lower = y_pred - y_pred * 0.14845856288 * 1.05**(x_smooth-2025)

    # Plotting
    plt.figure(figsize=(8, 5))
    plt.plot(x_smooth, y_pred, label='Exponential fit', color='green')
    plt.fill_between(x_smooth, y_lower, y_upper, color='green', alpha=0.2, label='50 % Confidence band')

    plt.ylim(0, max(y_pred) + 3000)
    plt.xlim(2024.75, 2030.25)
    plt.legend()
    plt.grid(True)
    plt.xlabel("Year")
    plt.ylabel("Predicted Car Price")
    plt.show()

    

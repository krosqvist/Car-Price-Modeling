import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from predictor import predict_car_price
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import io
import base64

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client['CarData']
collection = db['cars']


def grapher(model, maker, genmodel, reg_year, engin_size=None,
            gearbox=None, fuel_type=None, bodytype=None,
            miles=None):
    if miles is None:
        miles = (2025 - reg_year) * 7000
    else:
        miles = int(miles)

    x = []
    y = []

    for i in range(2025, 2031):
        # Use predict_car_price but pass MongoDB instead of CSV
        y_val = predict_car_price(
            model,
            maker,
            genmodel,
            reg_year,
            engin_size=engin_size,
            gearbox=gearbox,
            fuel_type=fuel_type,
            bodytype=bodytype,
            miles=miles + (i - 2025) * 7000,
            db_collection=collection,  # pass MongoDB collection instead of CSV path
            adv_year=i
        )
        x.append(i)
        y.append(y_val[0])

    x = np.array(x)
    y = np.array(y)

    # Define exponential model
    def exponential_model(x, a, b):
        return a * np.exp(-b * (x - 2025))

    # Fit exponential model
    try:
        popt, _ = curve_fit(exponential_model, x, y, maxfev=10000)
    except RuntimeError:
        print("Exponential fit failed. Falling back to linear fit.")
        return

    x_smooth = np.linspace(2024, 2031, 300)
    y_pred = exponential_model(x_smooth, *popt)

    y_upper = y_pred + 1750 * 1.02**(x_smooth - 2025)
    y_lower = y_pred - 1750 * 1.02**(x_smooth - 2025)

    plt.figure(figsize=(8, 5))
    plt.plot(x_smooth, y_pred, label='Exponential fit', color='green')
    plt.fill_between(x_smooth, y_lower, y_upper, color='green', alpha=0.2, label='50% Confidence band')
    plt.ylim(0, max(y_pred) + 3000)
    plt.xlim(2024.75, 2030.25)
    plt.legend()
    plt.grid(True)
    plt.xlabel("Year")
    plt.ylabel("Predicted Car Price")
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    print(f"__IMG__START__{img_base64}__IMG__END__")

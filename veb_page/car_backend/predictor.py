import pandas as pd

def predict_car_price(model, maker, genmodel, reg_year, engin_size=None,
                      gearbox=None, fuel_type=None, bodytype=None,
                      miles=None, db_collection=None, adv_year=None):
    """
    Predict car price using a trained model and MongoDB as data source.

    Parameters
    ----------
    model : sklearn-like trained model
    maker : str
    genmodel : str
    reg_year : int
    engin_size : float, optional
    gearbox : str, optional
    fuel_type : str, optional
    bodytype : str, optional
    miles : int, optional
    db_collection : pymongo.collection.Collection, required
        MongoDB collection containing car data
    adv_year : int, optional
        Year to predict for. Defaults to 2025.

    Returns
    -------
    tuple
        (predicted price, entry price used)
    """
    if adv_year is None:
        adv_year = 2025

    vehicle_age = adv_year - reg_year
    if miles is None:
        miles = vehicle_age * 7000
    else:
        miles = int(miles)

    # --- Query MongoDB for Entry_price ---
    entry_price_doc = db_collection.find_one(
        {'Genmodel_ID': str(genmodel), 'Reg_year': int(reg_year)},
        {'Entry_price': 1, '_id': 0}
    )

    if entry_price_doc and 'Entry_price' in entry_price_doc:
        entry_price = entry_price_doc['Entry_price']
    else:
        # fallback to maker-level median
        maker_doc = db_collection.find({'Maker': maker}, {'Entry_price': 1, '_id': 0})
        maker_prices = [doc['Entry_price'] for doc in maker_doc if 'Entry_price' in doc]
        if maker_prices:
            entry_price = float(pd.Series(maker_prices).median())
        else:
            entry_price = 20000  # final fallback

    # --- Inflation index (hardcoded fallback if needed) ---
    inflation_index = {
        2030: 0.8943, 2029: 0.9122, 2028: 0.9305, 2027: 0.9491,
        2026: 0.9690, 2025: 1.0000, 2024: 1.0327, 2023: 1.1028,
        2022: 1.1902, 2021: 1.2202, 2020: 1.2322, 2019: 1.2537,
        2018: 1.2824, 2017: 1.3152, 2016: 1.3285, 2015: 1.3334,
        2014: 1.3527, 2013: 1.3837, 2012: 1.4193, 2011: 1.4741,
        2010: 1.5108, 2009: 1.5404, 2008: 1.5946, 2007: 1.6327,
        2006: 1.6729, 2005: 1.7078, 2004: 1.7316, 2003: 1.7555,
        2002: 1.7822, 2001: 1.8094, 2000: 1.8308, 1999: 1.8628,
        1998: 1.8967, 1997: 1.9385, 1996: 1.9937, 1995: 2.0475
    }

    # --- Build row for prediction ---
    row = pd.DataFrame([{
        'Maker': maker,
        'Genmodel': genmodel,
        'Gearbox': gearbox if gearbox else 'Automatic',
        'Fuel_type': fuel_type if fuel_type else 'Petrol',
        'Bodytype': bodytype if bodytype else 'SUV',
        'Engin_size': engin_size if engin_size else 1.6,
        'Adv_year': adv_year,
        'Reg_year': reg_year,
        'Vehicle_age': vehicle_age,
        'Runned_Miles': miles,
        'Entry_price': entry_price
    }])

    return float(model.predict(row)[0])/inflation_index[adv_year], entry_price

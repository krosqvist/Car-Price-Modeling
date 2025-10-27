import pandas as pd

def predict_car_price(model, maker, genmodel, reg_year, engin_size=None,
                      gearbox=None, fuel_type=None, bodytype=None,
                      miles=None, data_path='data/grouped_cars.csv', adv_year=None):
    """
    note:\n
    model : sklearn-like trained model
        (for example: car_price_model.pkl).
    maker : str
    genmodel : str
    reg_year : int
    engine_size : int
    gearbox : str
    fuel_type : str
        Fuel types: 'Diesel' 'Petrol' 'Petrol Ethanol'
        'Hybrid  Petrol/Electric' 'Bi Fuel' 'Hybrid  Petrol/Electric Plug-in'
        'Petrol Hybrid' 'Petrol Plug-in Hybrid' 'Hybrid  Diesel/Electric'
        'Hybrid  Diesel/Electric Plug-in' 'Diesel Hybrid'
    bodytype : str, optional
        Car body types: 
        'MPV' 'Hatchback' 'Coupe' 'Estate' 
        'Convertible' 'SUV' 'Car Derived Van' 'Panel Van' 
        'Saloon' 'Pickup' 'Combi Van' 'Window Van'
    miles : int
    data_path : str
        Path to the full dataset
    adv_year : int
        If adv_year isn't given, it defaults to 2025
    """
    # set the used advertisement year if missing
    if adv_year is None:
        adv_year=2025

    vehicle_age = adv_year - reg_year


    df = pd.read_csv(data_path)
    
    # find an appropriate entry price for the vehicle
    entry_price = None
    mask = (df['Genmodel_ID'] == genmodel) & (df['Reg_year'] == reg_year)
    if mask.any():
        entry_price = df.loc[mask, 'Entry_price'].median()
    if entry_price is None or pd.isna(entry_price):
        mask_maker = (df['Maker'] == maker)
        if mask_maker.any():
            entry_price = df.loc[mask_maker, 'Entry_price'].median()
    if entry_price is None or pd.isna(entry_price):
        entry_price = 25000

    # https://www.macrotrends.net/global-metrics/countries/gbr/united-kingdom/inflation-rate-cpi
    inflation_index = {
        2030: 0.8943,
        2029: 0.9122,
        2028: 0.9305,
        2027: 0.9491,
        2026: 0.9690,
        2025: 1.0000,
        2024: 1.0327,
        2023: 1.1028,
        2022: 1.1902,
        2021: 1.2202,
        2020: 1.2322,
        2019: 1.2537,
        2018: 1.2824,
        2017: 1.3152,
        2016: 1.3285,
        2015: 1.3334,
        2014: 1.3527,
        2013: 1.3837,
        2012: 1.4193,
        2011: 1.4741,
        2010: 1.5108,
        2009: 1.5404,
        2008: 1.5946,
        2007: 1.6327,
        2006: 1.6729,
        2005: 1.7078,
        2004: 1.7316,
        2003: 1.7555,
        2002: 1.7822,
        2001: 1.8094,
        2000: 1.8308,
        1999: 1.8628,
        1998: 1.8967,
        1997: 1.9385,
        1996: 1.9937,
        1995: 2.0475
    }

    row = pd.DataFrame([{
        'Maker': maker,
        'Genmodel': genmodel,
        'Gearbox': gearbox if gearbox is not None else 'Automatic',
        'Fuel_type': fuel_type if fuel_type is not None else 'Petrol',
        'Bodytype': bodytype if bodytype is not None else 'SUV',
        'Engin_size': engin_size if engin_size is not None else 1.6,
        'Adv_year': adv_year,
        'Reg_year': reg_year,
        'Vehicle_age': vehicle_age,
        'Runned_Miles': miles if miles is not None else vehicle_age*7000,
        'Entry_price': entry_price,
    }])

    # Adjustment for inflation
    return (float(model.predict(row)[0])/inflation_index[adv_year], entry_price)

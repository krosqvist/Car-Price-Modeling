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
        Fuel types: 'Diesel' 'Petrol' nan 'Petrol Ethanol' 'Electric'
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
    if adv_year is None:
        adv_year=2025

    vehicle_age = adv_year - reg_year


    df = pd.read_csv(data_path)
    
    entry_price = None
    mask = (df['Genmodel_ID'] == genmodel) & (df['Reg_year'] == reg_year)
    if mask.any():
        entry_price = df.loc[mask, 'Entry_price'].median()
    if entry_price is None or pd.isna(entry_price):
        mask_maker = (df['Maker'] == maker)
        if mask_maker.any():
            entry_price = df.loc[mask_maker, 'Entry_price'].median()
    if entry_price is None or pd.isna(entry_price):
        entry_price = 10000

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
        'Runned_Miles': miles if miles is not None else 50000,
        'Entry_price': entry_price,
        'Inflation_index': 0
    }])

    return print(f'Estimated price: {float(model.predict(row)[0])}\nEntry price: {entry_price}')

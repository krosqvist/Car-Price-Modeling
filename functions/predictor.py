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
        adv_year = 2025

    vehicle_age = adv_year - reg_year

    df = pd.read_csv(data_path)

    mask = (df['Genmodel_ID'] == genmodel) & (df['Reg_year'] == reg_year)
    if mask.any():
        entry_price = df.loc[mask, 'Entry_price'].median()
        infl_index_entry = df.loc[mask, 'Inflation_index_entry'].median()
    else:
        mask_maker = (df['Maker'] == maker)
        if mask_maker.any():
            entry_price = df.loc[mask_maker, 'Entry_price'].median()
            infl_index_entry = df.loc[mask_maker, 'Inflation_index_entry'].median()
        else:
            entry_price = 25000
            infl_index_entry = df['Inflation_index_entry'].mean()

    mask_adv = df['Adv_year'] == adv_year
    infl_index_adv = df.loc[mask_adv, 'Inflation_index'].median() if mask_adv.any() else df['Inflation_index'].mean()

    row = pd.DataFrame([{
        'Maker': maker,
        'Genmodel': genmodel,
        'Gearbox': gearbox or 'Automatic',
        'Fuel_type': fuel_type or 'Petrol',
        'Bodytype': bodytype or 'SUV',
        'Engin_size': engin_size or 1.6,
        'Adv_year': adv_year,
        'Reg_year': reg_year,
        'Vehicle_age': vehicle_age,
        'Runned_Miles': miles or (vehicle_age * 7100),
        'Entry_price': entry_price,
        'Inflation_index': infl_index_adv,
        'Inflation_index_entry': infl_index_entry
    }])

    return print(f'Estimated price: {float(model.predict(row)[0])}\nEntry price: {entry_price}')

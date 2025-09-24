import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

df = pd.read_csv("grouped_cars.csv")

df['Vehicle_age'] = df['Adv_year'] - df['Reg_year']

categorical_features = ['Maker', 'Genmodel', 'Fuel_type']
numerical_features = ['Engin_size', 'Vehicle_age', 'km', 'Inflation_index']

X = df[categorical_features + numerical_features]
y = df['Price']

# Ei hyvä strategia välttämättä. Väliaikainen
numeric_transformer = SimpleImputer(strategy='mean')  

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')), 
    ('onehot', OneHotEncoder(handle_unknown='ignore'))     
])

preprocessor = ColumnTransformer(transformers=[
    ('num', numeric_transformer, numerical_features),
    ('cat', categorical_transformer, categorical_features)
])

model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(
        n_estimators=500,  
        max_depth=None,      
        random_state=42,
        n_jobs=-1
    ))
])


#############################################################################################

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model.fit(X_train, y_train)


y_pred = model.predict(X_test)

#testi
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
print(f"Mean Squared Error: {mse}")
print(f"Root Mean Squared Error: {rmse}")

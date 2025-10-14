###############################################################################
# Define paths
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
data_path = os.path.join(base_dir, 'data', 'grouped_cars.csv')
###############################################################################


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import numpy as np
import joblib

df = pd.read_csv(data_path)


categorical_features = ['Engin_size','Maker', 'Genmodel','Reg_year', 'Gearbox', 'Fuel_type', 'Bodytype']
numerical_features = ['Vehicle_age', 'Runned_Miles', 'Entry_price']

# 'Maker', 'Genmodel_ID','Gearbox', 'Fuel_type', 'Bodytype'
# 'Engin_size', 'Vehicle_age', 'km', 'Entry_price', 'Inflation_index'



X = df[categorical_features + numerical_features]
y = df['Price']

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
        n_estimators=200,  
        max_depth=30,      
        random_state=42,
        n_jobs=-1
    ))
])


#############################################################################################

X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.2, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Fit model
model.fit(X_train, y_train)

# the model is saved to the previous folder
joblib.dump(model, 'car_price_model.pkl')

# Evaluate
y_val_pred = model.predict(X_val)
val_rmse = np.sqrt(mean_squared_error(y_val, y_val_pred))
print(f"Validation RMSE: {val_rmse:.2f}")

y_test_pred = model.predict(X_test)
test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
r2 = r2_score(y_test, y_test_pred)
print(f"Test RMSE: {test_rmse:.2f}")
print(f"Test R²: {r2:.3f}")


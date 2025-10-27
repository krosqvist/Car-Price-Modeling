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
numerical_features = ['Vehicle_age', 'Runned_Miles', 'Entry_price', 'Inflation_index']

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



#############################################################################################

X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.2, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

from functions.hyperparameter_finder import rf_tree_depth_est
rmse_n_estimators_max_depth= rf_tree_depth_est(preprocessor, train_data=X_train, train_targ=y_train, val_data=X_val, val_targ=y_val, maxtrees=250)
best_t = rmse_n_estimators_max_depth[1]
best_d = rmse_n_estimators_max_depth[2]
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(
        n_estimators=100,  
        max_depth=30,      
        random_state=42,
        n_jobs=-1
    ))
])

model2 = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(
        n_estimators=best_t,  
        max_depth=best_d,      
        random_state=42,
        n_jobs=-1
    ))
])

# Fit model
model.fit(X_train, y_train)
model2.fit(X_train, y_train)

# Evaluate
y_val_pred = model.predict(X_val)
val_rmse = np.sqrt(mean_squared_error(y_val, y_val_pred))
print(f"Validation RMSE: {val_rmse:.2f}")

y_val_pred = model2.predict(X_val)
val_rmse = np.sqrt(mean_squared_error(y_val, y_val_pred))
print(f"Validation RMSE: {val_rmse:.2f}")

y_test_pred = model.predict(X_test)
test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
r2 = r2_score(y_test, y_test_pred)
print(f"Test RMSE: {test_rmse:.2f}")
print(f"Test R²: {r2:.3f}")

y_test_pred = model2.predict(X_test)
test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
r2 = r2_score(y_test, y_test_pred)
print(f"Test RMSE: {test_rmse:.2f}")
print(f"Test R²: {r2:.3f}")

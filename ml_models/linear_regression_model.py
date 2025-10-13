###############################################################################
# Define paths
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
data_path = os.path.join(base_dir, 'data', 'grouped_cars.csv')
###############################################################################


from sklearn.preprocessing import OneHotEncoder, PowerTransformer
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge
from sklearn.compose import TransformedTargetRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pandas as pd
import joblib

df = pd.read_csv(data_path)

categorical_features = ['Maker', 'Genmodel', 'Reg_year', 'Adv_year', 'Gearbox', 'Fuel_type', 'Bodytype']
numerical_features = ['Engin_size', 'Runned_Miles', 'Entry_price', 'Inflation_index', 'Inflation_index_entry']

# Split the data 
X = df[categorical_features + numerical_features]
y = df['Price']

#################################################################################
# Processing
numericFix = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('transform', PowerTransformer())
])

categoricalFix = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(transformers=[
    ('num', numericFix, numerical_features),
    ('cat', categoricalFix, categorical_features)
])
#################################################################################


# Base model
ridge = Ridge(alpha=1.0)

# Wrap in target transformer
model = TransformedTargetRegressor(
    regressor=Pipeline(steps=[('preprocessor', preprocessor), ('regressor', ridge)]),
    func=np.log1p, inverse_func=np.expm1  # data-driven for exponential decay
)


################################################################################
# Split data to training, test, and evaluation parts.
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.2, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

model.fit(X_train, y_train)
joblib.dump(model, 'car_price_model_linear.pkl')



y_val_pred = model.predict(X_val)
val_rmse = np.sqrt(mean_squared_error(y_val, y_val_pred))
print(f"Validation RMSE: {val_rmse:.2f}")

y_test_pred = model.predict(X_test)
test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
r2 = r2_score(y_test, y_test_pred)
print(f"Test RMSE: {test_rmse:.2f}")
print(f"Test R²: {r2:.3f}")

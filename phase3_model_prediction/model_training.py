import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
from model_utils import evaluate_and_save_best_model

# Load your cleaned and indexed dataset
df = pd.read_csv('AirQualityUCI.csv', sep=';', decimal=',')
# Combine date and time, set datetime index
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H.%M.%S', errors='coerce')
df = df.set_index('Datetime')

# Convert all columns to numeric first
df = df.apply(pd.to_numeric, errors='coerce')

# Replace -200 with NaN in CO(GT)
df['CO(GT)'] = df['CO(GT)'].replace(-200, np.nan)

# Drop rows with missing CO values
df = df[['CO(GT)']].dropna()

print("Data shape after feature engineering and dropna:", df.shape)
print("Rows remaining after preprocessing:", len(df))

# Feature Engineering
df['Hour'] = df.index.hour
df['Day'] = df.index.day
df['Month'] = df.index.month
df['CO_lag1'] = df['CO(GT)'].shift(1)
df['CO_lag2'] = df['CO(GT)'].shift(2)
df['CO_roll3'] = df['CO(GT)'].rolling(3).mean()
df['CO_std3'] = df['CO(GT)'].rolling(3).std()
df.dropna(inplace=True)

# Split into train and test sets
split_index = int(len(df) * 0.8)
train = df.iloc[:split_index]
test = df.iloc[split_index:]

X_train = train.drop(columns=['CO(GT)'])
y_train = train['CO(GT)']
X_test = test.drop(columns=['CO(GT)'])
y_test = test['CO(GT)']

# Train models
lr = LinearRegression().fit(X_train, y_train)
rf = RandomForestRegressor(n_estimators=100).fit(X_train, y_train)
xgb = XGBRegressor().fit(X_train, y_train)

# Evaluation function
def evaluate(model, name):
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    print(f"{name} - MAE: {mae:.2f}, RMSE: {rmse:.2f}")

evaluate(lr, "Linear Regression")
evaluate(rf, "Random Forest")
evaluate(xgb, "XGBoost")

models = {
    "Linear Regression": lr,
    "Random Forest": rf,
    "XGBoost": xgb
}

# Evaluate all and save the best one
best_model = evaluate_and_save_best_model(models, X_test, y_test)

# Save best model
joblib.dump(best_model, 'co_forecast_model.pkl')
print("Model saved as 'co_forecast_model.pkl'")

#Baseline comparison
baseline_preds = X_test['CO_lag1']  # because you already engineered this feature
baseline_mae = mean_absolute_error(y_test, baseline_preds)
baseline_rmse = np.sqrt(mean_squared_error(y_test, baseline_preds))

print(f"Baseline Model (Previous Value) - MAE: {baseline_mae:.2f}, RMSE: {baseline_rmse:.2f}")

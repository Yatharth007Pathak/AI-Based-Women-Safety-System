# CRIME RISK PREDICTION MODEL TRAINING

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


# LOAD DATASET
DATA_PATH = "../../dataset/crime_data.csv"

print("Loading crime dataset...")

data = pd.read_csv(DATA_PATH)

# Features and Target
X = data[["latitude", "longitude"]]
y = data["risk_score"]

print("Dataset loaded successfully.")
print(f"Total records: {len(data)}")


# TRAIN TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# TRAIN MODEL
print("Training Random Forest model...")

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)


# EVALUATION
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\nModel Evaluation:")
print("Mean Absolute Error:", mae)
print("R2 Score:", r2)


# SAVE MODEL
joblib.dump(model, "crime_model.pkl")

print("\nModel saved as crime_model.pkl")
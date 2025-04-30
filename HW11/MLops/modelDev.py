import os
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pickle

# --- Config ---
CSV_PATH = '50_Startups.csv'
MODEL_PATH = '../HW11/MLops/model.pkl'

# --- Load Data ---
df = pd.read_csv(CSV_PATH)

# Features and target
X = df.drop("Profit", axis=1)
y = df["Profit"]

# Preprocessing: OneHotEncode 'State', passthrough numerical columns
preprocessor = ColumnTransformer(
    transformers=[('cat', OneHotEncoder(drop='first'), ['State'])],
    remainder='passthrough'
)

# Full pipeline
model = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

# Train and save
model.fit(X, y)

with open(MODEL_PATH, 'wb') as f:
    pickle.dump(model, f)

print(f"✅ Model trained and saved as {MODEL_PATH}")

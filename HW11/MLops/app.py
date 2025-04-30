from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# Load the trained model and expected column order
model = joblib.load("model.pkl")
columns = joblib.load("columns.pkl")  # ['R&D Spend', 'Administration', 'Marketing Spend', 'State_Florida', 'State_New York']

# Define FastAPI app
app = FastAPI()

# Define request schema
class StartupData(BaseModel):
    RnD_Spend: float
    Administration: float
    Marketing_Spend: float
    State: str  # Accepts "California", "Florida", or "New York"

# Define prediction endpoint
@app.post("/predict")
def predict(data: StartupData):
    # One-hot encode state (California is baseline: 0,0)
    state_florida = int(data.State == "Florida")
    state_new_york = int(data.State == "New York")

    # Assemble feature dictionary
    input_dict = {
        'R&D Spend': float(data.RnD_Spend),
        'Administration': float(data.Administration),
        'Marketing Spend': float(data.Marketing_Spend),
        'State_Florida': state_florida,
        'State_New York': state_new_york
    }

    # Create DataFrame in the correct column order
    input_df = pd.DataFrame([input_dict])[columns]

    # Predict and return result
    prediction = model.predict(input_df)[0]
    return {"predicted_profit": prediction}
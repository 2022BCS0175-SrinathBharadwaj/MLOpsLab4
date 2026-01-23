from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Create FastAPI app FIRST
app = FastAPI(title="Wine Quality Prediction API")

# Load trained model
model = joblib.load("model.joblib")

# Input schema
class WineInput(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float

@app.get("/")
def home():
    return {"message": "Wine Quality Prediction API is running"}

@app.post("/predict")
def predict(data: WineInput):
    features = np.array([[
        data.fixed_acidity,
        data.volatile_acidity,
        data.citric_acid,
        data.residual_sugar,
        data.chlorides,
        data.free_sulfur_dioxide,
        data.total_sulfur_dioxide,
        data.density,
        data.pH,
        data.sulphates,
        data.alcohol
    ]])

    prediction = model.predict(features)

    return {
        "name": "Srinath Bharadwaj",
        "roll_no": "2022BCS0175",
        "wine_quality": int(round(prediction[0]))
    }

import joblib

model = joblib.load(
    "models/misinformation_model.pkl"
)

scaler = joblib.load(
    "models/risk_scaler.pkl"
)
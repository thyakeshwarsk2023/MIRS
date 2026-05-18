import streamlit as st
import joblib


@st.cache_resource
def load_models():

    model = joblib.load(
        "models/misinformation_model.pkl"
    )

    scaler = joblib.load(
        "models/risk_scaler.pkl"
    )

    return model, scaler


model, scaler = load_models()
"""Cached article analysis pipeline — preserves existing ML logic."""

import hashlib
import streamlit as st
import joblib
from sentence_transformers import SentenceTransformer

from src.preprocess import preprocess_text
from src.emotion import analyze_emotion
from src.propoganda import detect_propaganda, propaganda_score
from src.credibillity import calculate_risk


@st.cache_resource(show_spinner=False)
def _load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


@st.cache_resource(show_spinner=False)
def _load_classifier():
    model = joblib.load("models/misinformation_model.pkl")
    scaler = joblib.load("models/risk_scaler.pkl")
    return model, scaler


def _risk_label(misinformation_risk: float) -> str:
    if misinformation_risk >= 70:
        return "HIGH RISK NARRATIVE"
    if misinformation_risk >= 40:
        return "MODERATE RISK NARRATIVE"
    return "LOW RISK NARRATIVE"


def run_analysis(article_text: str) -> dict:
    """
    Core analysis — same logic as original app.analyze_article.
    Model inference is not cached here so each Analyze click re-runs on edited text.
    """
    cleaned_text = preprocess_text(article_text)
    embedding_model = _load_embedding_model()
    model, scaler = _load_classifier()

    embedding = embedding_model.encode([cleaned_text])
    model.predict(embedding)

    misinformation_risk = calculate_risk(model, scaler, embedding)
    prediction_label = _risk_label(misinformation_risk)

    emotion_analysis = analyze_emotion(article_text)
    propaganda_matches = detect_propaganda(article_text)
    propaganda_risk = propaganda_score(propaganda_matches)

    return {
        "prediction": prediction_label,
        "misinformation_risk": misinformation_risk,
        "emotion_type": emotion_analysis["emotion_type"],
        "emotion_intensity": emotion_analysis["emotion_intensity"],
        "negative_emotion": emotion_analysis["negative_score"],
        "neutral_tone": emotion_analysis["neutral_score"],
        "positive_emotion": emotion_analysis["positive_score"],
        "propaganda_signals": propaganda_matches,
        "propaganda_risk": propaganda_risk,
    }


@st.cache_data(show_spinner=False, ttl=3600)
def cached_ai_summary(analysis_key: str, analysis: dict) -> str:
    """Cache LLM responses per analysis fingerprint to avoid repeat API calls on rerender."""
    from src.llm_explainer import generate_ai_explanation

    return generate_ai_explanation(analysis)


def analysis_fingerprint(article_text: str, analysis: dict) -> str:
    payload = f"{article_text}|{analysis['misinformation_risk']}|{analysis['propaganda_risk']}"
    return hashlib.sha256(payload.encode()).hexdigest()[:16]

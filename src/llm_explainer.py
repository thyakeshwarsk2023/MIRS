import streamlit as st
from openai import OpenAI


# =====================================================
# LOAD OPENROUTER CLIENT
# =====================================================

@st.cache_resource
def load_client():

    return OpenAI(

        base_url="https://openrouter.ai/api/v1",

        api_key=st.secrets[
            "OPENROUTER_API_KEY"
        ]
    )


client = load_client()


# =====================================================
# AI ANALYST SUMMARY
# =====================================================

def generate_ai_explanation(analysis):

    risk = analysis["misinformation_risk"]

    emotion = analysis["emotion_type"]

    propaganda = analysis["propaganda_risk"]

    prompt = f"""
    You are a cybersecurity and
    misinformation analyst.

    Analyze the following
    narrative-risk indicators
    and produce a concise
    professional intelligence summary.

    Rules:
    - Maximum 80 words
    - Professional tone
    - No repetition
    - No markdown
    - No bullet points
    - Clear concise analysis

    Narrative Classification:
    {analysis['prediction']}

    Risk Score:
    {risk}%

    Emotion Type:
    {emotion}

    Emotional Intensity:
    {analysis['emotion_intensity']}%

    Negative Emotional Pressure:
    {analysis['negative_emotion']}%

    Propaganda Signals:
    {analysis['propaganda_signals']}

    Propaganda Risk:
    {propaganda}%
    """

    try:

        response = client.chat.completions.create(

            model=
            "meta-llama/llama-3.1-8b-instruct:free",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.3,

            max_tokens=120
        )

        return response.choices[
            0
        ].message.content.strip()

    except Exception:

        # =============================================
        # LOCAL FALLBACK SUMMARY
        # =============================================

        if risk >= 70:

            return (
                "The narrative demonstrates "
                "strong indicators of emotional "
                "manipulation, persuasive framing, "
                "and elevated misinformation-risk "
                "characteristics. Emotional pressure "
                "and propaganda-related rhetoric "
                "suggest attempts to influence "
                "reader perception through "
                "high-intensity narrative framing."
            )

        elif risk >= 40:

            return (
                "The article exhibits moderate "
                "narrative-risk characteristics. "
                "Emotional persuasion patterns "
                "and rhetorical amplification "
                "were identified, indicating "
                "potential sensationalized framing "
                "without strong manipulation signals."
            )

        else:

            return (
                "The narrative demonstrates "
                "relatively low misinformation-risk "
                "characteristics. Linguistic tone "
                "appears comparatively neutral with "
                "limited emotional amplification "
                "or propaganda-style persuasion "
                "patterns detected."
            )
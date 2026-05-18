import html
import hashlib
import re
import streamlit as st

st.set_page_config(
    page_title="MIRS - Narrative Intelligence System",
    page_icon="🧠",
    layout="wide"
)

import joblib
from pypdf import PdfReader
import trafilatura
from sentence_transformers import SentenceTransformer

from src.preprocess import preprocess_text
from src.emotion import analyze_emotion
from src.propoganda import detect_propaganda, propaganda_score, get_phrase_explanation
from src.credibillity import calculate_risk
from src.llm_explainer import generate_ai_explanation
from src.highlighting import highlight_propaganda_text


# =========================================================
# CACHED LOADERS
# =========================================================

@st.cache_resource(show_spinner=False)
def _load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


@st.cache_resource(show_spinner=False)
def _load_classifier():
    model  = joblib.load("models/misinformation_model.pkl")
    scaler = joblib.load("models/risk_scaler.pkl")
    return model, scaler


# =========================================================
# HELPERS
# =========================================================

def get_risk_color(risk: float) -> str:
    if risk >= 70:
        return "#ff4b4b"
    if risk >= 40:
        return "#ffb703"
    return "#00c853"


def get_risk_label(risk: float) -> str:
    if risk >= 70:
        return "HIGH RISK NARRATIVE"
    if risk >= 40:
        return "MODERATE RISK NARRATIVE"
    return "LOW RISK NARRATIVE"


def safe_html(value) -> str:
    return html.escape(str(value))


def clean_ai_summary(raw: str) -> str:
    text = str(raw).strip()
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*",     r"\1", text)
    text = re.sub(r"__(.*?)__",     r"\1", text)
    text = re.sub(r"_(.*?)_",       r"\1", text)
    text = html.escape(text)
    text = text.replace("\n", "<br>")
    return text


def analysis_fingerprint(article_text: str, analysis: dict) -> str:
    payload = (
        article_text
        + "|" + str(analysis["misinformation_risk"])
        + "|" + str(analysis["propaganda_risk"])
    )
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def build_bar_html(label: str, value: float, color: str) -> str:
    """
    Build a single progress-bar row using plain string concatenation.
    Avoids f-string quote conflicts that caused Streamlit to render
    raw HTML text instead of actual rendered HTML.
    """
    return (
        '<div style="margin-bottom:22px;">'
        '<div style="display:flex;justify-content:space-between;'
        'margin-bottom:8px;font-size:15px;color:#d1d5db;">'
        "<span>" + label + "</span>"
        '<span style="font-weight:700;color:white;">' + str(value) + "%</span>"
        "</div>"
        '<div style="background:#1f2937;height:14px;'
        'border-radius:999px;overflow:hidden;">'
        '<div style="width:' + str(value) + "%;background:" + color + ";"
        'height:100%;border-radius:999px;"></div>'
        "</div>"
        "</div>"
    )


# =========================================================
# CORE ANALYSIS
# =========================================================

def run_analysis(article_text: str) -> dict:
    cleaned_text    = preprocess_text(article_text)
    embedding_model = _load_embedding_model()
    model, scaler   = _load_classifier()

    embedding           = embedding_model.encode([cleaned_text])
    misinformation_risk = calculate_risk(model, scaler, embedding)
    prediction_label    = get_risk_label(misinformation_risk)

    emotion_analysis   = analyze_emotion(article_text)
    propaganda_matches = detect_propaganda(article_text)
    propaganda_risk    = propaganda_score(propaganda_matches)

    return {
        "prediction":          prediction_label,
        "misinformation_risk": round(float(misinformation_risk), 2),
        "emotion_type":        emotion_analysis["emotion_type"],
        "emotion_intensity":   emotion_analysis["emotion_intensity"],
        "negative_emotion":    emotion_analysis["negative_score"],
        "neutral_tone":        emotion_analysis["neutral_score"],
        "positive_emotion":    emotion_analysis["positive_score"],
        "propaganda_signals":  propaganda_matches,
        "propaganda_risk":     propaganda_risk,
        "risk_color":          get_risk_color(misinformation_risk),
    }


@st.cache_data(show_spinner=False, ttl=3600)
def cached_ai_summary(fingerprint: str, analysis: dict) -> str:
    return generate_ai_explanation(analysis)


# =========================================================
# GLOBAL CSS
# =========================================================

st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #081120;
    color: white;
    font-family: "Inter", sans-serif;
}
.stApp {
    background: radial-gradient(circle at top, #13203a 0%, #081120 45%);
    color: white;
}
.block-container {
    padding-top: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
    padding-bottom: 2rem;
}
.hero-card {
    background: linear-gradient(135deg, rgba(255,75,75,0.10), rgba(255,183,3,0.05));
    border: 1px solid rgba(255,255,255,0.08);
    padding: 45px;
    border-radius: 28px;
    margin-bottom: 2rem;
    backdrop-filter: blur(12px);
    box-shadow: 0px 0px 35px rgba(255,75,75,0.10);
}
.hero-top {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 18px;
    flex-wrap: wrap;
}
.hero-logo {
    font-size: 74px;
    filter: drop-shadow(0px 0px 14px rgba(255,75,75,0.45));
}
.hero-title {
    font-size: 64px;
    font-weight: 800;
    background: linear-gradient(90deg, #ff4b4b, #ffb703);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
}
.hero-subtitle {
    font-size: 22px;
    color: #d1d5db;
    margin-bottom: 25px;
    max-width: 900px;
    line-height: 1.7;
}
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 16px;
    margin-top: 20px;
}
.feature-item {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
    padding: 18px;
    border-radius: 18px;
    font-size: 15px;
    color: #e5e7eb;
    line-height: 1.7;
    transition: 0.3s;
}
.feature-item:hover {
    transform: translateY(-3px);
    background: rgba(255,255,255,0.06);
}
textarea {
    background-color: #111827 !important;
    color: white !important;
    border-radius: 16px !important;
    border: 1px solid #2a3441 !important;
    font-size: 16px !important;
}
input {
    background-color: #111827 !important;
    color: white !important;
    border-radius: 14px !important;
}
.stButton > button {
    background: linear-gradient(90deg, #ff4b4b, #ff6b6b);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 12px 28px;
    font-size: 17px;
    font-weight: 600;
    transition: 0.3s;
}
.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0px 0px 22px rgba(255,75,75,0.35);
}
[data-testid="metric-container"] {
    background: #121b2b;
    border: 1px solid #263041;
    padding: 20px;
    border-radius: 18px;
}
hr { border-color: #1f2937; }
.mirs-article-body {
    font-size: 16px;
    line-height: 1.9;
    color: #d1d5db;
    white-space: pre-wrap;
    word-wrap: break-word;
}
.mirs-highlight {
    background: rgba(255, 75, 75, 0.18);
    border-bottom: 2px solid #ff4b4b;
    border-radius: 4px;
    padding: 1px 3px;
    cursor: help;
    position: relative;
}
.mirs-highlight-tag {
    font-size: 10px;
    color: #ff4b4b;
    margin-left: 2px;
    vertical-align: super;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="hero-card">
  <div class="hero-top">
    <div class="hero-logo">&#x1F9E0;</div>
    <div class="hero-title">MIRS</div>
  </div>
  <div class="hero-subtitle">
    AI-Powered Narrative Intelligence &amp; Misinformation Risk Detection Platform
  </div>
  <div class="feature-grid">
    <div class="feature-item">&#x26A1; Detect misinformation-style narratives</div>
    <div class="feature-item">&#x1F9E0; Analyze emotional manipulation tactics</div>
    <div class="feature-item">&#x1F6A8; Detect propaganda-related rhetoric</div>
    <div class="feature-item">&#x1F575;&#xFE0F; Generate AI analyst interpretations</div>
    <div class="feature-item">&#x1F310; Scan live article URLs instantly</div>
    <div class="feature-item">&#x1F4C4; Upload and analyze PDF documents</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.divider()


# =========================================================
# INPUT SECTION
# =========================================================

st.subheader("📰 Article Intelligence Input")
st.markdown("""
Choose one of the following input methods:
- Paste a live news URL
- Upload a PDF article
- Manually paste article text
""")

article_text = ""

tab1, tab2, tab3 = st.tabs(["🌐 URL", "📄 PDF", "✍️ Manual Text"])

with tab1:
    article_url = st.text_input(
        "Paste Article URL",
        placeholder="https://example.com/article"
    )
    if article_url:
        with st.spinner("Extracting article..."):
            try:
                downloaded     = trafilatura.fetch_url(article_url)
                extracted_text = trafilatura.extract(downloaded)
                if extracted_text:
                    article_text = extracted_text
                    st.success("Article extracted successfully.")
                else:
                    st.error("Could not extract article content.")
            except Exception as e:
                st.error("Extraction failed: " + str(e))
    if article_text:
        article_text = st.text_area(
            "Extracted Article Content", article_text, height=350
        )

with tab2:
    uploaded_file = st.file_uploader("Upload PDF Document", type=["pdf"])
    if uploaded_file is not None:
        with st.spinner("Reading PDF..."):
            pdf_reader     = PdfReader(uploaded_file)
            extracted_text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    extracted_text += page_text
            article_text = st.text_area(
                "Extracted PDF Content", extracted_text, height=350
            )

with tab3:
    manual_text = st.text_area(
        "Paste Article Content",
        height=350,
        placeholder="Paste article text here for analysis..."
    )
    if manual_text:
        article_text = manual_text

st.write("")
analyze_button = st.button("🚀 Analyze Narrative")


# =========================================================
# MAIN ANALYSIS
# =========================================================

if analyze_button:

    if not article_text.strip():
        st.warning("Please enter article content.")

    else:
        with st.spinner("🧠 Analyzing narrative intelligence..."):
            analysis     = run_analysis(article_text)
            fingerprint  = analysis_fingerprint(article_text, analysis)
            raw_summary  = cached_ai_summary(fingerprint, analysis)
            safe_summary = clean_ai_summary(raw_summary)

        risk_color = analysis["risk_color"]
        risk_score = analysis["misinformation_risk"]
        prediction = analysis["prediction"]


        # --------------------------------------------------
        # HERO RISK CARD
        # --------------------------------------------------

        hero_html = (
            '<div style="background:linear-gradient(135deg,'
            + risk_color + ',#121b2b);'
            'padding:42px;border-radius:28px;color:white;text-align:center;'
            'margin-bottom:20px;border:1px solid rgba(255,255,255,0.08);'
            'box-shadow:0px 0px 35px rgba(0,0,0,0.35);">'
            '<div style="font-size:14px;letter-spacing:2px;color:#d7d7d7;'
            'margin-bottom:14px;font-weight:600;">AI NARRATIVE RISK ANALYSIS</div>'
            '<h1 style="font-size:52px;font-weight:800;margin-bottom:16px;'
            'line-height:1.2;color:white;">'
            + safe_html(prediction) +
            '</h1>'
            '<div style="font-size:22px;font-weight:600;margin-bottom:30px;color:white;">'
            'Risk Score: <span style="font-size:38px;font-weight:800;">'
            + str(risk_score) + '%</span></div>'
            '<div style="display:flex;justify-content:center;gap:20px;flex-wrap:wrap;">'
            '<div style="background:rgba(255,255,255,0.08);padding:18px 24px;'
            'border-radius:20px;min-width:260px;">'
            '<div style="font-size:13px;letter-spacing:1px;color:#d7d7d7;margin-bottom:10px;">'
            'EMOTIONAL MANIPULATION</div>'
            '<div style="font-size:22px;font-weight:700;line-height:1.5;color:white;">'
            + safe_html(analysis["emotion_type"]) +
            '</div></div>'
            '<div style="background:rgba(255,255,255,0.08);padding:18px 24px;'
            'border-radius:20px;min-width:220px;">'
            '<div style="font-size:13px;letter-spacing:1px;color:#d7d7d7;margin-bottom:10px;">'
            'PROPAGANDA RISK</div>'
            '<div style="font-size:34px;font-weight:800;color:white;">'
            + str(analysis["propaganda_risk"]) + '%</div>'
            '</div></div></div>'
        )
        st.markdown(hero_html, unsafe_allow_html=True)


        # --------------------------------------------------
        # EXECUTIVE SUMMARY
        # --------------------------------------------------

        st.subheader("📌 Executive Risk Summary")

        exec_html = (
            '<div style="background:rgba(255,255,255,0.04);'
            'border:1px solid rgba(255,255,255,0.06);padding:24px;'
            'border-radius:20px;color:#d1d5db;font-size:17px;'
            'line-height:1.9;margin-bottom:10px;">'
            'This narrative demonstrates '
            '<b>' + safe_html(str(analysis["emotion_type"]).lower()) + '</b>'
            ' with an emotional intensity of '
            '<b>' + str(analysis["emotion_intensity"]) + '%</b>.'
            '<br><br>'
            'Semantic credibility analysis indicates a misinformation risk score of '
            '<b>' + str(risk_score) + '%</b>.'
            '<br><br>'
            'Propaganda analysis identified '
            '<b>' + str(len(analysis["propaganda_signals"])) + '</b>'
            ' rhetorical manipulation indicators associated with narrative persuasion patterns.'
            '</div>'
        )
        st.markdown(exec_html, unsafe_allow_html=True)

        st.divider()


        # --------------------------------------------------
        # EMOTIONAL ANALYSIS — 3 COLUMNS
        # --------------------------------------------------

        st.subheader("🧠 Emotional Manipulation Analysis")

        ec1, ec2, ec3 = st.columns(3)

        with ec1:
            st.markdown(
                '<div style="background:#121b2b;padding:24px;border-radius:20px;'
                'border:1px solid #263041;min-height:140px;">'
                '<div style="color:#9ca3af;font-size:14px;margin-bottom:12px;letter-spacing:1px;">'
                'EMOTION TYPE</div>'
                '<div style="font-size:24px;font-weight:700;line-height:1.4;color:white;">'
                + safe_html(analysis["emotion_type"]) + '</div></div>',
                unsafe_allow_html=True
            )

        with ec2:
            st.markdown(
                '<div style="background:#121b2b;padding:24px;border-radius:20px;'
                'border:1px solid #263041;min-height:140px;">'
                '<div style="color:#9ca3af;font-size:14px;margin-bottom:12px;letter-spacing:1px;">'
                'EMOTIONAL INTENSITY</div>'
                '<div style="font-size:42px;font-weight:800;color:#ffb703;">'
                + str(analysis["emotion_intensity"]) + '%</div></div>',
                unsafe_allow_html=True
            )

        with ec3:
            st.markdown(
                '<div style="background:#121b2b;padding:24px;border-radius:20px;'
                'border:1px solid #263041;min-height:140px;">'
                '<div style="color:#9ca3af;font-size:14px;margin-bottom:12px;letter-spacing:1px;">'
                'NEGATIVE TONE</div>'
                '<div style="font-size:42px;font-weight:800;color:#ff4b4b;">'
                + str(analysis["negative_emotion"]) + '%</div></div>',
                unsafe_allow_html=True
            )

        st.write("")


        # --------------------------------------------------
        # RISK TAGS
        # --------------------------------------------------

        st.subheader("🏷️ Narrative Risk Tags")

        tags = []
        if analysis["emotion_intensity"] > 70:
            tags.append("EMOTIONAL MANIPULATION")
        if analysis["propaganda_risk"] > 30:
            tags.append("PROPAGANDA SIGNALS")
        if analysis["negative_emotion"] > 20:
            tags.append("FEAR AMPLIFICATION")
        if risk_score > 70:
            tags.append("HIGH RISK NARRATIVE")
        if risk_score < 40:
            tags.append("LOW CREDIBILITY RISK")

        if not tags:
            st.success("No major narrative-risk indicators detected.")
        else:
            tag_spans = ""
            for tag in tags:
                tag_spans += (
                    '<span style="display:inline-block;'
                    'background:linear-gradient(90deg,#ff4b4b,#ff7b54);'
                    'color:white;padding:10px 18px;border-radius:999px;'
                    'margin-right:10px;margin-bottom:10px;font-size:13px;'
                    'font-weight:700;letter-spacing:0.5px;'
                    'box-shadow:0px 0px 12px rgba(255,75,75,0.18);">'
                    + safe_html(tag) + '</span>'
                )
            st.markdown(
                '<div style="padding:4px 0;margin-bottom:10px;">'
                + tag_spans + '</div>',
                unsafe_allow_html=True
            )

        st.write("")


        # --------------------------------------------------
        # EMOTIONAL TONE DISTRIBUTION  — FIXED
        # --------------------------------------------------

        st.subheader("📊 Emotional Tone Distribution")

        bar1 = build_bar_html(
            "Negative Emotional Pressure",
            analysis["negative_emotion"],
            "#ff4b4b"
        )
        bar2 = build_bar_html(
            "Neutral Tone",
            analysis["neutral_tone"],
            "#94a3b8"
        )
        bar3 = build_bar_html(
            "Positive Tone",
            analysis["positive_emotion"],
            "#00c853"
        )

        st.markdown(
            '<div style="margin-bottom:10px;">' + bar1 + bar2 + bar3 + '</div>',
            unsafe_allow_html=True
        )

        st.divider()


        # --------------------------------------------------
        # NARRATIVE RISK ASSESSMENT
        # --------------------------------------------------

        st.subheader("⚠️ Narrative Risk Assessment")

        risk_html = (
            '<div style="background:linear-gradient(135deg,'
            'rgba(255,255,255,0.04),rgba(255,255,255,0.02));'
            'padding:30px;border-radius:24px;'
            'border:1px solid rgba(255,255,255,0.06);margin-bottom:10px;">'
            '<div style="display:flex;justify-content:space-between;'
            'align-items:center;flex-wrap:wrap;gap:20px;margin-bottom:18px;">'
            '<div>'
            '<div style="font-size:14px;letter-spacing:1px;color:#9ca3af;margin-bottom:6px;">'
            'CURRENT THREAT LEVEL</div>'
            '<div style="font-size:34px;font-weight:800;color:' + risk_color + ';">'
            + safe_html(prediction) + '</div>'
            '</div>'
            '<div style="font-size:54px;font-weight:900;color:white;">'
            + str(round(risk_score, 1)) + '%</div>'
            '</div>'
            '<div style="background:#1f2937;height:18px;border-radius:999px;overflow:hidden;">'
            '<div style="width:' + str(risk_score) + '%;background:' + risk_color + ';'
            'height:100%;border-radius:999px;"></div>'
            '</div>'
            '<p style="color:#cbd5e1;margin-top:18px;font-size:15px;line-height:1.8;">'
            'Narrative risk scoring combines: semantic credibility analysis, '
            'emotional manipulation intensity, and propaganda-related persuasion patterns.'
            '</p></div>'
        )
        st.markdown(risk_html, unsafe_allow_html=True)

        st.divider()


        # --------------------------------------------------
        # PROPAGANDA INDICATORS
        # --------------------------------------------------

        st.subheader("🚨 Propaganda Indicators")

        signals = analysis["propaganda_signals"]

        if signals:
            signals_html = ""
            for signal in signals:
                explanation = safe_html(get_phrase_explanation(signal))
                signals_html += (
                    '<div style="background:rgba(255,75,75,0.08);'
                    'border:1px solid rgba(255,75,75,0.15);'
                    'padding:14px 18px;border-radius:16px;margin-bottom:12px;">'
                    '<div style="color:#ffb4b4;font-size:15px;font-weight:700;margin-bottom:6px;">'
                    '&#x1F6A9; ' + safe_html(signal) + '</div>'
                    '<div style="color:#9ca3af;font-size:13px;line-height:1.6;">'
                    + explanation + '</div>'
                    '</div>'
                )
            st.markdown(
                '<div style="margin-bottom:10px;">' + signals_html + '</div>',
                unsafe_allow_html=True
            )
        else:
            st.success("No major propaganda indicators detected.")

        st.divider()


        # --------------------------------------------------
        # HIGHLIGHTED ARTICLE VIEW
        # --------------------------------------------------

        st.subheader("🔦 Narrative Manipulation Highlight Map")

        st.markdown(
            '<div style="color:#9ca3af;font-size:14px;margin-bottom:16px;">'
            'Detected rhetorical phrases are highlighted below. '
            'Hover over any highlight to see the analyst explanation.'
            '</div>',
            unsafe_allow_html=True
        )

        highlighted_html = highlight_propaganda_text(article_text, signals)

        st.markdown(
            '<div style="background:rgba(255,255,255,0.03);'
            'border:1px solid rgba(255,255,255,0.06);'
            'padding:28px;border-radius:20px;margin-bottom:10px;'
            'max-height:420px;overflow-y:auto;">'
            + highlighted_html + '</div>',
            unsafe_allow_html=True
        )

        st.divider()


        # --------------------------------------------------
        # AI ANALYST INTERPRETATION
        # --------------------------------------------------

        st.subheader("🕵️ Analyst Interpretation")

        st.markdown(
            '<div style="background:linear-gradient(135deg,#161616,#202020);'
            'padding:32px;border-radius:24px;border-left:6px solid #ff4b4b;'
            'box-shadow:0px 0px 25px rgba(255,75,75,0.12);margin-bottom:10px;">'
            '<div style="font-size:15px;letter-spacing:1px;color:#9ca3af;margin-bottom:14px;">'
            'AI-GENERATED INTELLIGENCE SUMMARY</div>'
            '<div style="color:#f3f4f6;font-size:17px;line-height:1.9;">'
            + safe_summary + '</div>'
            '</div>',
            unsafe_allow_html=True
        )

        st.divider()


        # --------------------------------------------------
        # RAW ARTICLE EXPANDER
        # --------------------------------------------------

        with st.expander("📄 View Submitted Article"):
            st.write(article_text)

        st.divider()


        # --------------------------------------------------
        # DISCLAIMER
        # --------------------------------------------------

        st.markdown(
            '<div style="color:#9ca3af;font-size:14px;line-height:1.8;padding-bottom:20px;">'
            '&#x26A0;&#xFE0F; This system evaluates emotional, linguistic, and propaganda-related '
            'narrative risk patterns using NLP and AI-based analysis models. '
            'It does not perform objective fact verification or determine '
            'absolute factual accuracy.'
            '</div>',
            unsafe_allow_html=True
        )
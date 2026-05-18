import streamlit as st
import plotly.graph_objects as go
from pypdf import PdfReader
import trafilatura
from src.preprocess import preprocess_text
from src.emotion import analyze_emotion
from src.propoganda import (
    detect_propaganda,
    propaganda_score
)
from src.embeddings import embedding_model
from src.classifier import (
    model,
    scaler
)
from src.credibillity import calculate_risk
from src.llm_explainer import (
    generate_ai_explanation
)


# =========================================================
# PAGE CONFIG
# =========================================================

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="MIRS - Narrative Intelligence System",
    page_icon="🧠",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* ================================
GLOBAL
================================ */

html,
body,
[class*="css"] {

    background-color: #081120;

    color: white;

    font-family: "Inter", sans-serif;
}

/* Main App Background */

.stApp {

    background:
    radial-gradient(
        circle at top,
        #13203a 0%,
        #081120 45%
    );

    color: white;
}

/* Main Container */

.block-container {

    padding-top: 2rem;

    padding-left: 3rem;

    padding-right: 3rem;

    padding-bottom: 2rem;
}

/* ================================
HERO SECTION
================================ */

.hero-card {

    background:
    linear-gradient(
        135deg,
        rgba(255,75,75,0.10),
        rgba(255,183,3,0.05)
    );

    border:
    1px solid rgba(255,255,255,0.08);

    padding: 45px;

    border-radius: 28px;

    margin-bottom: 2rem;

    backdrop-filter: blur(12px);

    box-shadow:
    0px 0px 35px rgba(255,75,75,0.10);
}

/* Hero Layout */

.hero-top {

    display: flex;

    align-items: center;

    gap: 20px;

    margin-bottom: 18px;

    flex-wrap: wrap;
}

/* Logo */

.hero-logo {

    font-size: 74px;

    filter:
    drop-shadow(
        0px 0px 14px rgba(255,75,75,0.45)
    );
}

/* Main Title */

.hero-title {

    font-size: 64px;

    font-weight: 800;

    background:
    linear-gradient(
        90deg,
        #ff4b4b,
        #ffb703
    );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;

    line-height: 1;
}

/* Subtitle */

.hero-subtitle {

    font-size: 22px;

    color: #d1d5db;

    margin-bottom: 25px;

    max-width: 900px;

    line-height: 1.7;
}

/* Feature Grid */

.feature-grid {

    display: grid;

    grid-template-columns:
    repeat(auto-fit, minmax(240px, 1fr));

    gap: 16px;

    margin-top: 20px;
}

/* Feature Card */

.feature-item {

    background:
    rgba(255,255,255,0.04);

    border:
    1px solid rgba(255,255,255,0.06);

    padding: 18px;

    border-radius: 18px;

    font-size: 15px;

    color: #e5e7eb;

    line-height: 1.7;

    transition: 0.3s;
}

.feature-item:hover {

    transform: translateY(-3px);

    background:
    rgba(255,255,255,0.06);
}

/* ================================
INPUTS
================================ */

textarea {

    background-color:
    #111827 !important;

    color:
    white !important;

    border-radius:
    16px !important;

    border:
    1px solid #2a3441 !important;

    font-size:
    16px !important;
}

/* Input fields */

input {

    background-color:
    #111827 !important;

    color:
    white !important;

    border-radius:
    14px !important;
}

/* Buttons */

.stButton > button {

    background:
    linear-gradient(
        90deg,
        #ff4b4b,
        #ff6b6b
    );

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

    box-shadow:
    0px 0px 22px rgba(255,75,75,0.35);
}

/* ================================
METRICS
================================ */

[data-testid="metric-container"] {

    background:
    #121b2b;

    border:
    1px solid #263041;

    padding: 20px;

    border-radius: 18px;
}

/* Divider */

hr {

    border-color: #1f2937;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="hero-card">

<div class="hero-top">

<div class="hero-logo">
🧠
</div>

<div class="hero-title">
MIRS
</div>

</div>

<div class="hero-subtitle">

AI-Powered Narrative Intelligence &
Misinformation Risk Detection Platform

</div>

<div class="feature-grid">

<div class="feature-item">
⚡ Detect misinformation-style narratives
</div>

<div class="feature-item">
🧠 Analyze emotional manipulation tactics
</div>

<div class="feature-item">
🚨 Detect propaganda-related rhetoric
</div>

<div class="feature-item">
🕵️ Generate AI analyst interpretations
</div>

<div class="feature-item">
🌐 Scan live article URLs instantly
</div>

<div class="feature-item">
📄 Upload and analyze PDF documents
</div>

</div>

</div>
""", unsafe_allow_html=True)

st.divider()

st.markdown("""
<div class="hero-card">

    <!-- Top Section -->
    <div style="
        display:flex;
        align-items:center;
        gap:20px;
        margin-bottom:18px;
        flex-wrap:wrap;
    ">

        <!-- Logo -->
        <div style="
            font-size:72px;
            filter:drop-shadow(
                0px 0px 14px rgba(255,75,75,0.45)
            );
        ">
            🧠
        </div>

        <!-- Title -->
        <div class="hero-title">
            MIRS
        </div>

    </div>

    <!-- Subtitle -->
    <div class="hero-subtitle">

        AI-Powered Narrative Intelligence &
        Misinformation Risk Detection Platform

    </div>

    <!-- Feature Grid -->
    <div style="
        display:grid;
        grid-template-columns:
        repeat(auto-fit, minmax(240px, 1fr));
        gap:16px;
        margin-top:25px;
    ">

        <div class="feature-item">
            ⚡ Detect misinformation-style narratives
        </div>

        <div class="feature-item">
            🧠 Analyze emotional manipulation tactics
        </div>

        <div class="feature-item">
            🚨 Detect propaganda-related rhetoric
        </div>

        <div class="feature-item">
            🕵️ Generate AI analyst interpretations
        </div>

        <div class="feature-item">
            🌐 Scan live article URLs instantly
        </div>

        <div class="feature-item">
            📄 Upload and analyze PDF documents
        </div>

    </div>

</div>
""", unsafe_allow_html=True)

st.divider()

# =========================================================
# ANALYSIS FUNCTION
# =========================================================
def get_risk_color(risk):

    if risk >= 70:
        return "#ff4b4b"

    elif risk >= 40:
        return "#ffb703"

    return "#00c853"


def get_risk_label(risk):

    if risk >= 70:
        return "HIGH RISK NARRATIVE"

    elif risk >= 40:
        return "MODERATE RISK NARRATIVE"

    return "LOW RISK NARRATIVE"


def analyze_article(article_text):

    # ==========================================
    # PREPROCESSING
    # ==========================================

    cleaned_text = preprocess_text(
        article_text
    )

    # ==========================================
    # EMBEDDING GENERATION
    # ==========================================

    embedding = embedding_model.encode(
        [cleaned_text]
    )

    # ==========================================
    # MODEL PREDICTION
    # ==========================================

    prediction = model.predict(
        embedding
    )[0]

    misinformation_risk = calculate_risk(
        model,
        scaler,
        embedding
    )

    prediction_label = get_risk_label(
        misinformation_risk
    )

    # ==========================================
    # EMOTIONAL ANALYSIS
    # ==========================================

    emotion_analysis = analyze_emotion(
        article_text
    )

    # ==========================================
    # PROPAGANDA ANALYSIS
    # ==========================================

    propaganda_matches = detect_propaganda(
        article_text
    )

    propaganda_risk = propaganda_score(
        propaganda_matches
    )

    # ==========================================
    # FINAL RESULT
    # ==========================================

    result = {

        "prediction":
        prediction_label,

        "misinformation_risk":
        round(misinformation_risk, 2),

        "emotion_type":
        emotion_analysis["emotion_type"],

        "emotion_intensity":
        emotion_analysis["emotion_intensity"],

        "negative_emotion":
        emotion_analysis["negative_score"],

        "neutral_tone":
        emotion_analysis["neutral_score"],

        "positive_emotion":
        emotion_analysis["positive_score"],

        "propaganda_signals":
        propaganda_matches,

        "propaganda_risk":
        propaganda_risk,

        "risk_color":
        get_risk_color(
            misinformation_risk
        )
    }

    return result

# =========================================================
# ARTICLE INPUT
# =========================================================
# =========================================================
# ARTICLE INPUT
# =========================================================

st.subheader(
    "📰 Article Intelligence Input"
)

st.markdown("""
Choose one of the following input methods:
- paste a live news URL
- upload a PDF article
- manually paste article text
""")


# ==========================================
# INPUT TABS
# ==========================================

tab1, tab2, tab3 = st.tabs([
    "🌐 URL",
    "📄 PDF",
    "✍️ Manual Text"
])


# ==========================================
# URL INPUT
# ==========================================

with tab1:

    article_url = st.text_input(
        "Paste Article URL",
        placeholder="https://example.com/article"
    )

    article_text = ""

    if article_url:

        with st.spinner(
            "Extracting article..."
        ):

            try:

                downloaded = trafilatura.fetch_url(
                    article_url
                )

                extracted_text = trafilatura.extract(
                    downloaded
                )

                if extracted_text:

                    article_text = extracted_text

                    st.success(
                        "Article extracted successfully."
                    )

                else:

                    st.error(
                        "Could not extract article content."
                    )

            except Exception as e:

                st.error(
                    f"Extraction failed: {e}"
                )

    if article_text:

        article_text = st.text_area(
            "Extracted Article Content",
            article_text,
            height=350
        )


# ==========================================
# PDF INPUT
# ==========================================

with tab2:

    uploaded_file = st.file_uploader(
        "Upload PDF Document",
        type=["pdf"]
    )

    if uploaded_file is not None:

        with st.spinner(
            "Reading PDF..."
        ):

            pdf_reader = PdfReader(
                uploaded_file
            )

            extracted_text = ""

            for page in pdf_reader.pages:

                page_text = page.extract_text()

                if page_text:

                    extracted_text += page_text

            article_text = st.text_area(
                "Extracted PDF Content",
                extracted_text,
                height=350
            )


# ==========================================
# MANUAL INPUT
# ==========================================

with tab3:

    manual_text = st.text_area(

        "Paste Article Content",

        height=350,

        placeholder="""
Paste article text here for
misinformation and narrative-risk analysis...
"""
    )

    if manual_text:

        article_text = manual_text


# ==========================================
# ANALYZE BUTTON
# ==========================================

st.write("")

analyze_button = st.button(
    "🚀 Analyze Narrative"
)

# =========================================================
# MAIN ANALYSIS
# =========================================================

# =========================================================
# MAIN ANALYSIS
# =========================================================

# =========================================================
# ANALYSIS EXECUTION
# =========================================================

if analyze_button:

    if not article_text.strip():

        st.warning(
            "Please enter article content."
        )

    else:

        with st.spinner(
            "🧠 Analyzing narrative intelligence..."
        ):

            analysis = analyze_article(
                article_text
            )

            ai_summary = generate_ai_explanation(
                analysis
            )

        # ==========================================
        # HERO RISK CARD
        # ==========================================

        risk_color = analysis["risk_color"]

        st.markdown(f"""
        <div style="

        background:
        linear-gradient(
            135deg,
            {risk_color},
            #121b2b
        );

        padding:42px;

        border-radius:28px;

        color:white;

        text-align:center;

        margin-bottom:30px;

        border:
        1px solid rgba(255,255,255,0.08);

        box-shadow:
        0px 0px 35px rgba(0,0,0,0.35);

        ">

        <!-- Small Label -->

        <div style="
            font-size:14px;
            letter-spacing:2px;
            color:#d7d7d7;
            margin-bottom:14px;
            font-weight:600;
        ">

        AI NARRATIVE RISK ANALYSIS

        </div>

        <!-- Main Prediction -->

        <h1 style="
            font-size:56px;
            font-weight:800;
            margin-bottom:16px;
            line-height:1.2;
        ">

        {analysis['prediction']}

        </h1>

        <!-- Risk Score -->

        <div style="
            font-size:22px;
            font-weight:600;
            margin-bottom:30px;
        ">

        Risk Score:

        <span style="
            font-size:38px;
            font-weight:800;
        ">
            {analysis['misinformation_risk']}%
        </span>

        </div>

        <!-- Insight Cards -->

        <div style="
            display:flex;
            justify-content:center;
            gap:20px;
            flex-wrap:wrap;
        ">

            <!-- Emotion -->

            <div style="
                background:
                rgba(255,255,255,0.08);

                padding:18px 24px;

                border-radius:20px;

                min-width:280px;
            ">

                <div style="
                    font-size:13px;
                    letter-spacing:1px;
                    color:#d7d7d7;
                    margin-bottom:10px;
                ">

                EMOTIONAL MANIPULATION

                </div>

                <div style="
                    font-size:22px;
                    font-weight:700;
                    line-height:1.5;
                ">

                {analysis['emotion_type']}

                </div>

            </div>

            <!-- Propaganda -->

            <div style="
                background:
                rgba(255,255,255,0.08);

                padding:18px 24px;

                border-radius:20px;

                min-width:240px;
            ">

                <div style="
                    font-size:13px;
                    letter-spacing:1px;
                    color:#d7d7d7;
                    margin-bottom:10px;
                ">

                PROPAGANDA RISK

                </div>

                <div style="
                    font-size:34px;
                    font-weight:800;
                ">

                {analysis['propaganda_risk']}%

                </div>

            </div>

        </div>

        </div>
        """, unsafe_allow_html=True)

        # ==========================================
        # EXECUTIVE SUMMARY
        # ==========================================

        st.subheader(
            "📌 Executive Risk Summary"
        )

        st.markdown(f"""
        <div style="

        background:
        rgba(255,255,255,0.04);

        border:
        1px solid rgba(255,255,255,0.06);

        padding:24px;

        border-radius:20px;

        color:#d1d5db;

        font-size:17px;

        line-height:1.9;

        margin-bottom:25px;

        ">

        This narrative demonstrates
        <b>{analysis['emotion_type'].lower()}</b>
        with an emotional intensity of
        <b>{analysis['emotion_intensity']}%</b>.

        <br><br>

        Semantic credibility analysis indicates a
        misinformation risk score of
        <b>{analysis['misinformation_risk']}%</b>.

        <br><br>

        Propaganda analysis identified
        <b>{len(analysis['propaganda_signals'])}</b>
        rhetorical manipulation indicators
        associated with narrative persuasion patterns.

        </div>
        """, unsafe_allow_html=True)

        st.divider()


        # =================================================
        # EXECUTIVE SUMMARY
        # =================================================

        st.subheader(
            "📌 Executive Risk Summary"
        )

        summary_text = f"""

        This article demonstrates
        {analysis['emotion_type'].lower()}
        with an emotional intensity of
        {analysis['emotion_intensity']}%.

        The narrative exhibits a
        misinformation risk score of
        {analysis['misinformation_risk']}%.

        Propaganda analysis detected
        {len(analysis['propaganda_signals'])}
        high-risk rhetorical indicators.

        """

        st.info(summary_text)

        st.divider()

        # =================================================
        # EMOTIONAL ANALYSIS
        # =================================================

        # =========================================================
# EMOTIONAL ANALYSIS
# =========================================================

st.subheader(
    "🧠 Emotional Manipulation Analysis"
)

emotion_col1, emotion_col2, emotion_col3 = st.columns(3)

with emotion_col1:

    st.markdown(f"""
    <div style="
        background:#121b2b;
        padding:24px;
        border-radius:20px;
        border:1px solid #263041;
        height:160px;
    ">

    <div style="
        color:#9ca3af;
        font-size:14px;
        margin-bottom:12px;
        letter-spacing:1px;
    ">
    EMOTION TYPE
    </div>

    <div style="
        font-size:26px;
        font-weight:700;
        line-height:1.4;
        color:white;
    ">
    {analysis["emotion_type"]}
    </div>

    </div>
    """, unsafe_allow_html=True)

with emotion_col2:

    st.markdown(f"""
    <div style="
        background:#121b2b;
        padding:24px;
        border-radius:20px;
        border:1px solid #263041;
        height:160px;
    ">

    <div style="
        color:#9ca3af;
        font-size:14px;
        margin-bottom:12px;
        letter-spacing:1px;
    ">
    EMOTIONAL INTENSITY
    </div>

    <div style="
        font-size:42px;
        font-weight:800;
        color:#ffb703;
    ">
    {analysis['emotion_intensity']}%
    </div>

    </div>
    """, unsafe_allow_html=True)

with emotion_col3:

    st.markdown(f"""
    <div style="
        background:#121b2b;
        padding:24px;
        border-radius:20px;
        border:1px solid #263041;
        height:160px;
    ">

    <div style="
        color:#9ca3af;
        font-size:14px;
        margin-bottom:12px;
        letter-spacing:1px;
    ">
    NEGATIVE TONE
    </div>

    <div style="
        font-size:42px;
        font-weight:800;
        color:#ff4b4b;
    ">
    {analysis['negative_emotion']}%
    </div>

    </div>
    """, unsafe_allow_html=True)

st.write("")


# =========================================================
# RISK TAGS
# =========================================================

st.subheader(
    "🏷️ Narrative Risk Tags"
)

tags = []

if analysis["emotion_intensity"] > 70:
    tags.append("EMOTIONAL MANIPULATION")

if analysis["propaganda_risk"] > 30:
    tags.append("PROPAGANDA SIGNALS")

if analysis["negative_emotion"] > 20:
    tags.append("FEAR AMPLIFICATION")

if analysis["misinformation_risk"] > 70:
    tags.append("HIGH RISK NARRATIVE")

if analysis["misinformation_risk"] < 40:
    tags.append("LOW CREDIBILITY RISK")

if len(tags) == 0:

    st.success(
        "No major narrative-risk indicators detected."
    )

else:

    tags_html = ""

    for tag in tags:

        tags_html += f"""
        <span style="
            display:inline-block;
            background:
            linear-gradient(
                90deg,
                #ff4b4b,
                #ff7b54
            );

            color:white;

            padding:10px 18px;

            border-radius:999px;

            margin-right:10px;

            margin-bottom:10px;

            font-size:13px;

            font-weight:700;

            letter-spacing:0.5px;

            box-shadow:
            0px 0px 12px rgba(255,75,75,0.18);
        ">
        {tag}
        </span>
        """

    st.markdown(
        tags_html,
        unsafe_allow_html=True
    )

st.write("")

# =========================================================
# EMOTIONAL TONE METER
# =========================================================

st.subheader(
    "📊 Emotional Tone Distribution"
)

emotion_data = [

    (
        "Negative Emotional Pressure",
        analysis["negative_emotion"],
        "#ff4b4b"
    ),

    (
        "Neutral Tone",
        analysis["neutral_tone"],
        "#94a3b8"
    ),

    (
        "Positive Tone",
        analysis["positive_emotion"],
        "#00c853"
    )
]

for label, value, color in emotion_data:

    st.markdown(f"""
    <div style="
        margin-bottom:22px;
    ">

        <div style="
            display:flex;
            justify-content:space-between;
            margin-bottom:8px;
            font-size:15px;
            color:#d1d5db;
        ">

            <span>{label}</span>

            <span style="
                font-weight:700;
                color:white;
            ">
            {value}%
            </span>

        </div>

        <div style="
            background:#1f2937;
            height:14px;
            border-radius:999px;
            overflow:hidden;
        ">

            <div style="
                width:{value}%;
                background:{color};
                height:100%;
                border-radius:999px;
                transition:0.4s;
            ">
            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)

st.divider()


# =========================================================
# NARRATIVE RISK ASSESSMENT
# =========================================================

st.subheader(
    "⚠️ Narrative Risk Assessment"
)

risk = analysis["misinformation_risk"]

risk_label = analysis["prediction"]

risk_color = analysis["risk_color"]

st.markdown(f"""
<div style="

background:
linear-gradient(
    135deg,
    rgba(255,255,255,0.04),
    rgba(255,255,255,0.02)
);

padding:30px;

border-radius:24px;

border:
1px solid rgba(255,255,255,0.06);

margin-top:15px;

margin-bottom:10px;

">

<div style="
    display:flex;
    justify-content:space-between;
    align-items:center;
    flex-wrap:wrap;
    gap:20px;
    margin-bottom:18px;
">

    <div>

        <div style="
            font-size:14px;
            letter-spacing:1px;
            color:#9ca3af;
            margin-bottom:6px;
        ">

        CURRENT THREAT LEVEL

        </div>

        <div style="
            font-size:34px;
            font-weight:800;
            color:{risk_color};
        ">

        {risk_label}

        </div>

    </div>

    <div style="
        font-size:54px;
        font-weight:900;
        color:white;
    ">

    {risk:.1f}%

    </div>

</div>

<div style="
    background:#1f2937;
    height:18px;
    border-radius:999px;
    overflow:hidden;
">

    <div style="
        width:{risk}%;
        background:{risk_color};
        height:100%;
        border-radius:999px;
        transition:0.5s;
    ">
    </div>

</div>

<p style="
    color:#cbd5e1;
    margin-top:18px;
    font-size:15px;
    line-height:1.8;
">

Narrative risk scoring combines:
semantic credibility analysis,
emotional manipulation intensity,
and propaganda-related persuasion patterns.

</p>

</div>
""", unsafe_allow_html=True)

st.divider()


# =========================================================
# PROPAGANDA INDICATORS
# =========================================================

st.subheader(
    "🚨 Propaganda Indicators"
)

signals = analysis["propaganda_signals"]

if len(signals) > 0:

    signal_html = ""

    for signal in signals:

        signal_html += f"""
        <div style="
            background:
            rgba(255,75,75,0.08);

            border:
            1px solid rgba(255,75,75,0.15);

            padding:14px 18px;

            border-radius:16px;

            color:#ffb4b4;

            font-size:15px;

            font-weight:600;

            margin-bottom:12px;
        ">

        🚩 {signal}

        </div>
        """

    st.markdown(
        signal_html,
        unsafe_allow_html=True
    )

else:

    st.success(
        "No major propaganda indicators detected."
    )

st.divider()


# =========================================================
# AI ANALYST INTERPRETATION
# =========================================================

st.subheader(
    "🕵️ Analyst Interpretation"
)

st.markdown(f"""
<div style="

background:
linear-gradient(
    135deg,
    #161616,
    #202020
);

padding:32px;

border-radius:24px;

border-left:
6px solid #ff4b4b;

box-shadow:
0px 0px 25px rgba(255,75,75,0.12);

margin-top:15px;

margin-bottom:20px;

">

<div style="
    font-size:15px;
    letter-spacing:1px;
    color:#9ca3af;
    margin-bottom:14px;
">

AI-GENERATED INTELLIGENCE SUMMARY

</div>

<div style="
    color:#f3f4f6;
    font-size:17px;
    line-height:1.9;
">

{ai_summary}

</div>

</div>
""", unsafe_allow_html=True)

st.divider()


# =========================================================
# RAW ARTICLE
# =========================================================

with st.expander(
    "📄 View Submitted Article"
):

    st.write(article_text)

st.divider()


# =========================================================
# DISCLAIMER
# =========================================================

st.markdown("""
<div style="
    color:#9ca3af;
    font-size:14px;
    line-height:1.8;
    padding-bottom:20px;
">

⚠️ This system evaluates emotional,
linguistic, and propaganda-related
narrative risk patterns using NLP
and AI-based analysis models.

It does not perform objective
fact verification or determine
absolute factual accuracy.

</div>
""", unsafe_allow_html=True)
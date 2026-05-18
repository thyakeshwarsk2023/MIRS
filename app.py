"""
MIRS — Misinformation & Narrative Intelligence Platform
Streamlit intelligence dashboard entry point.
"""

import streamlit as st
from pypdf import PdfReader
import trafilatura

from src.ui.theme import inject_theme
from src.ui.components import (
    render_hero_header,
    render_risk_hero,
    render_executive_summary,
    render_emotion_cards,
    render_risk_tags,
    render_emotion_gauge,
    render_narrative_risk_bar,
    render_propaganda_indicators,
    render_analyst_interpretation,
    render_narrative_highlight,
    render_disclaimer,
)
from src.analysis_pipeline import (
    run_analysis,
    cached_ai_summary,
    analysis_fingerprint,
)
from src.highlighting import highlight_propaganda_text


st.set_page_config(
    page_title="MIRS — Narrative Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_theme()
render_hero_header()
st.divider()


# ---------------------------------------------------------------------------
# Article input
# ---------------------------------------------------------------------------

st.markdown('<p class="mirs-section-label">Intelligence Input</p>', unsafe_allow_html=True)
st.markdown('<div class="mirs-input-panel">', unsafe_allow_html=True)

input_mode = st.radio(
    "Source",
    ["URL Scrape", "PDF Upload", "Manual Text"],
    horizontal=True,
    label_visibility="collapsed",
)

article_text = ""

if input_mode == "URL Scrape":
    article_url = st.text_input(
        "Article URL",
        placeholder="https://example.com/news-article",
    )
    if article_url:
        try:
            downloaded = trafilatura.fetch_url(article_url)
            extracted = trafilatura.extract(downloaded) or ""
            if not extracted:
                st.error("Could not extract article content from this URL.")
            article_text = st.text_area(
                "Extracted content (editable)",
                value=extracted,
                height=320,
                key="mirs_url_text",
            )
        except Exception as exc:
            st.error(f"Extraction failed: {exc}")
            article_text = st.text_area(
                "Paste article content",
                height=320,
                key="mirs_url_fallback",
            )
    else:
        article_text = st.text_area(
            "Article content",
            height=320,
            placeholder="Enter a URL above or paste text here…",
            key="mirs_url_empty",
        )

elif input_mode == "PDF Upload":
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_file is not None:
        pdf_reader = PdfReader(uploaded_file)
        extracted_pdf = "".join(
            page.extract_text() or "" for page in pdf_reader.pages
        )
        article_text = st.text_area(
            "Extracted PDF content (editable)",
            value=extracted_pdf,
            height=320,
            key="mirs_pdf_text",
        )
    else:
        article_text = st.text_area(
            "PDF content",
            height=320,
            placeholder="Upload a PDF document…",
            key="mirs_pdf_empty",
        )

else:
    article_text = st.text_area(
        "Article text",
        height=320,
        placeholder="Paste news article text here for narrative threat analysis…",
        key="mirs_manual_text",
    )

st.markdown("</div>", unsafe_allow_html=True)

col_btn, _ = st.columns([1, 4])
with col_btn:
    analyze_button = st.button("▶ Run Analysis", type="primary", use_container_width=True)


# ---------------------------------------------------------------------------
# Analysis results
# ---------------------------------------------------------------------------

if analyze_button:
    text_to_analyze = (article_text or "").strip()

    if not text_to_analyze:
        st.warning("Please provide article text before running analysis.")
    else:
        with st.spinner("Running narrative intelligence pipeline…"):
            analysis = run_analysis(text_to_analyze)
            fp = analysis_fingerprint(text_to_analyze, analysis)
            ai_summary = cached_ai_summary(fp, analysis)
            highlighted_html = highlight_propaganda_text(
                text_to_analyze,
                analysis["propaganda_signals"],
            )

        st.divider()
        render_risk_hero(analysis)
        render_executive_summary(analysis)
        st.divider()

        render_emotion_cards(analysis)
        render_risk_tags(analysis)
        render_emotion_gauge(analysis)
        st.divider()

        render_narrative_risk_bar(analysis)
        st.divider()

        render_propaganda_indicators(analysis)
        st.divider()

        render_narrative_highlight(
            text_to_analyze,
            analysis["propaganda_signals"],
            highlighted_html,
        )
        st.divider()

        render_analyst_interpretation(ai_summary)
        st.divider()

        with st.expander("📄 Submitted Article (raw)"):
            st.write(text_to_analyze)

        render_disclaimer()

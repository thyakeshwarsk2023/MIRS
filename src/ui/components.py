"""Reusable MIRS dashboard UI blocks."""

import html
import streamlit as st
import plotly.graph_objects as go


def render_hero_header():
    st.markdown(
        """
        <div class="mirs-hero-badge">Narrative Intelligence · v1</div>
        <h1 class="mirs-hero-title">MIRS</h1>
        <p class="mirs-hero-sub">
            Misinformation &amp; Narrative Intelligence Platform —
            analyst-grade threat assessment for digital narratives
        </p>
        <div class="mirs-features">
            <span class="mirs-feature-pill">Misinformation Risk</span>
            <span class="mirs-feature-pill">Emotional Manipulation</span>
            <span class="mirs-feature-pill">Propaganda Rhetoric</span>
            <span class="mirs-feature-pill">AI Analyst Brief</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_risk_color(risk: float) -> str:
    if risk >= 70:
        return "#ff4757"
    if risk >= 40:
        return "#ffb703"
    return "#00e676"


def get_risk_label(risk: float) -> str:
    if risk >= 70:
        return "HIGH RISK"
    if risk >= 40:
        return "MODERATE RISK"
    return "LOW RISK"


def render_risk_hero(analysis: dict):
    risk = analysis["misinformation_risk"]
    color = get_risk_color(risk)

    st.markdown(
        f"""
        <div class="mirs-risk-hero" style="background: linear-gradient(135deg,
            {color}22 0%, {color}44 50%, {color}33 100%);
            border-color: {color}55;">
            <p class="mirs-section-label" style="color: rgba(255,255,255,0.7);
                margin-bottom: 0.5rem;">Threat Assessment</p>
            <h1>{html.escape(analysis['prediction'])}</h1>
            <div class="mirs-risk-score" style="color: {color};">{risk}%</div>
            <p style="margin: 0.25rem 0 0; opacity: 0.9; font-size: 0.95rem;">
                Narrative Misinformation Risk Score
            </p>
            <div class="mirs-risk-meta">
                <span><strong>Emotion:</strong> {html.escape(analysis['emotion_type'])}</span>
                <span><strong>Intensity:</strong> {analysis['emotion_intensity']}%</span>
                <span><strong>Propaganda:</strong> {analysis['propaganda_risk']}%</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_executive_summary(analysis: dict):
    st.markdown('<p class="mirs-section-label">Executive Brief</p>', unsafe_allow_html=True)
    signal_count = len(analysis["propaganda_signals"])
    plural = "s" if signal_count != 1 else ""
    emotion = html.escape(analysis["emotion_type"].lower())
    summary = (
        f"This article exhibits <strong>{emotion}</strong> "
        f"with emotional intensity at <strong>{analysis['emotion_intensity']}%</strong>. "
        f"Semantic credibility analysis assigns a misinformation risk of "
        f"<strong>{analysis['misinformation_risk']}%</strong>. "
        f"Rhetorical screening flagged <strong>{signal_count}</strong> "
        f"high-risk persuasive indicator{plural}."
    )
    st.markdown(
        f'<div class="mirs-card mirs-card-accent"><p style="margin:0;'
        f'color:#c5d0de;line-height:1.7;">{summary}</p></div>',
        unsafe_allow_html=True,
    )


def render_emotion_cards(analysis: dict):
    st.markdown(
        '<p class="mirs-section-label">Emotional Manipulation Analysis</p>',
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    metrics = [
        (c1, "Emotion Profile", analysis["emotion_type"]),
        (c2, "Intensity", f"{analysis['emotion_intensity']}%"),
        (c3, "Negative Pressure", f"{analysis['negative_emotion']}%"),
    ]
    for col, title, value in metrics:
        with col:
            st.markdown(
                f"""
                <div class="mirs-card">
                    <p class="mirs-card-title">{html.escape(title)}</p>
                    <p class="mirs-card-value">{html.escape(str(value))}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_risk_tags(analysis: dict):
    st.markdown('<p class="mirs-section-label">Risk Tags</p>', unsafe_allow_html=True)
    tags = []
    if analysis["emotion_intensity"] > 70:
        tags.append("EMOTIONAL MANIPULATION")
    if analysis["propaganda_risk"] > 30:
        tags.append("PROPAGANDA SIGNALS")
    if analysis["negative_emotion"] > 20:
        tags.append("FEAR AMPLIFICATION")
    if analysis["misinformation_risk"] > 70:
        tags.append("HIGH RISK NARRATIVE")

    if tags:
        tag_html = "".join(f'<span class="mirs-tag">{html.escape(t)}</span>' for t in tags)
        st.markdown(tag_html, unsafe_allow_html=True)
    else:
        st.markdown(
            '<span class="mirs-tag" style="border-color:#00e67655;color:#00e676;">'
            "LOW SIGNAL PROFILE</span>",
            unsafe_allow_html=True,
        )


def render_emotion_gauge(analysis: dict):
    st.markdown('<p class="mirs-section-label">Emotional Tone Spectrum</p>', unsafe_allow_html=True)

    fig = go.Figure()
    tones = [
        ("Negative", analysis["negative_emotion"], "#ff4757"),
        ("Neutral", analysis["neutral_tone"], "#8b9cb3"),
        ("Positive", analysis["positive_emotion"], "#00e676"),
    ]
    for i, (label, value, color) in enumerate(tones):
        pad = 0.04
        x0 = i / 3 + pad
        x1 = (i + 1) / 3 - pad
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=value,
                title={"text": label, "font": {"size": 13, "color": "#8b9cb3"}},
                number={"suffix": "%", "font": {"color": "#e8edf4"}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#444"},
                    "bar": {"color": color},
                    "bgcolor": "#1e2633",
                    "borderwidth": 0,
                },
                domain={"x": [x0, x1], "y": [0, 1]},
            )
        )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "IBM Plex Sans, sans-serif"},
        height=200,
        margin=dict(l=20, r=20, t=40, b=10),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_narrative_risk_bar(analysis: dict):
    st.markdown(
        '<p class="mirs-section-label">Narrative Risk Assessment</p>',
        unsafe_allow_html=True,
    )
    risk = analysis["misinformation_risk"]
    label = get_risk_label(risk)
    color = get_risk_color(risk)

    st.markdown(
        f"""
        <div class="mirs-card">
            <div style="display:flex;justify-content:space-between;align-items:center;
                margin-bottom:0.75rem;">
                <p class="mirs-card-value" style="font-size:1.15rem;">{label}</p>
                <p class="mirs-card-value" style="color:{color};font-family:'JetBrains Mono',monospace;">
                    {risk:.1f}%
                </p>
            </div>
            <div class="mirs-risk-bar-wrap">
                <div class="mirs-risk-bar-fill" style="width:{min(risk, 100)}%;
                    background:{color};"></div>
            </div>
            <p class="mirs-card-sub" style="margin-top:0.85rem;">
                Composite score from semantic credibility embeddings, emotional manipulation
                intensity, and propaganda-related rhetoric patterns.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_propaganda_indicators(analysis: dict):
    st.markdown(
        '<p class="mirs-section-label">Propaganda &amp; Rhetoric Indicators</p>',
        unsafe_allow_html=True,
    )
    signals = analysis["propaganda_signals"]

    if not signals:
        st.markdown(
            """
            <div class="mirs-card" style="border-color: rgba(0,230,118,0.3);">
                <p style="margin:0;color:#00e676;font-weight:500;">
                    No major propaganda indicators detected in this narrative.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    from src.propoganda import get_phrase_explanation

    cols = st.columns(2)
    for idx, signal in enumerate(signals):
        explanation = get_phrase_explanation(signal)
        with cols[idx % 2]:
            st.markdown(
                f"""
                <div class="mirs-signal-chip">
                    <p class="phrase">"{html.escape(signal)}"</p>
                    <p class="explain">{html.escape(explanation)}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_analyst_interpretation(ai_summary: str):
    st.markdown(
        '<p class="mirs-section-label">AI Analyst Interpretation</p>',
        unsafe_allow_html=True,
    )
    safe_summary = html.escape(ai_summary or "").replace("\n", "<br>")
    st.markdown(
        f"""
        <div class="mirs-analyst-panel">
            <h3>Analyst Brief</h3>
            <p>{safe_summary}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_narrative_highlight(article_text: str, matches: list[str], highlighted_html: str):
    st.markdown(
        '<p class="mirs-section-label">Narrative Manipulation Map</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="mirs-legend">
            <span><span class="swatch"></span> Flagged rhetorical phrase — hover for analyst note</span>
            <span>⚠ = persuasive / manipulative language pattern</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if matches:
        st.markdown(
            f'<div class="mirs-highlight-panel">{highlighted_html}</div>',
            unsafe_allow_html=True,
        )
        st.caption(
            f"{len(matches)} distinct rhetorical pattern(s) annotated. "
            "Highlighting maps detected phrases to known persuasion frameworks — "
            "not keyword spam filtering."
        )
    else:
        st.markdown(
            f"""
            <div class="mirs-highlight-panel">
                <p class="mirs-article-body">{html.escape(article_text[:8000])}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption("No high-risk rhetorical phrases detected for inline annotation.")


def render_disclaimer():
    st.markdown(
        """
        <div class="mirs-disclaimer">
            <strong>Disclaimer:</strong> MIRS evaluates emotional, linguistic, and
            propaganda-related narrative risk patterns using NLP and AI models.
            It does not perform objective factual verification or legal adjudication.
        </div>
        """,
        unsafe_allow_html=True,
    )

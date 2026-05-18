"""Global MIRS dashboard theme — dark cyber-intelligence aesthetic."""

THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --mirs-bg: #0a0e14;
    --mirs-surface: #111820;
    --mirs-surface-elevated: #161d28;
    --mirs-border: rgba(0, 212, 255, 0.12);
    --mirs-border-strong: rgba(0, 212, 255, 0.28);
    --mirs-accent: #00d4ff;
    --mirs-accent-dim: rgba(0, 212, 255, 0.15);
    --mirs-danger: #ff4757;
    --mirs-warning: #ffb703;
    --mirs-safe: #00e676;
    --mirs-text: #e8edf4;
    --mirs-muted: #8b9cb3;
    --mirs-radius: 14px;
    --mirs-radius-sm: 10px;
    --mirs-shadow: 0 8px 32px rgba(0, 0, 0, 0.45);
    --mirs-glow: 0 0 24px rgba(0, 212, 255, 0.08);
}

.stApp {
    background: linear-gradient(165deg, #0a0e14 0%, #0d1219 40%, #0a0f16 100%);
    font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

.block-container {
    padding-top: 1.25rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Hide default Streamlit chrome noise */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header[data-testid="stHeader"] {
    background: transparent;
}

/* Typography */
.mirs-hero-title {
    font-size: clamp(2rem, 4vw, 2.75rem);
    font-weight: 700;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #ffffff 0%, #00d4ff 55%, #7dd3fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.35rem 0;
    line-height: 1.15;
}

.mirs-hero-sub {
    font-size: 1.05rem;
    color: var(--mirs-muted);
    margin: 0 0 1rem 0;
    font-weight: 400;
    line-height: 1.5;
}

.mirs-hero-badge {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--mirs-accent);
    background: var(--mirs-accent-dim);
    border: 1px solid var(--mirs-border-strong);
    padding: 0.35rem 0.75rem;
    border-radius: 6px;
    margin-bottom: 0.85rem;
}

.mirs-section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--mirs-accent);
    margin-bottom: 0.5rem;
}

/* Feature pills */
.mirs-features {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 1rem 0 1.5rem 0;
}

.mirs-feature-pill {
    background: var(--mirs-surface-elevated);
    border: 1px solid var(--mirs-border);
    border-radius: 999px;
    padding: 0.4rem 0.9rem;
    font-size: 0.8rem;
    color: var(--mirs-text);
    box-shadow: var(--mirs-glow);
}

/* Cards */
.mirs-card {
    background: linear-gradient(145deg, var(--mirs-surface) 0%, var(--mirs-surface-elevated) 100%);
    border: 1px solid var(--mirs-border);
    border-radius: var(--mirs-radius);
    padding: 1.25rem 1.35rem;
    box-shadow: var(--mirs-shadow);
    margin-bottom: 0.75rem;
}

.mirs-card-accent {
    border-left: 3px solid var(--mirs-accent);
}

.mirs-card-title {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--mirs-muted);
    margin: 0 0 0.35rem 0;
}

.mirs-card-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--mirs-text);
    margin: 0;
    line-height: 1.2;
}

.mirs-card-sub {
    font-size: 0.8rem;
    color: var(--mirs-muted);
    margin: 0.35rem 0 0 0;
}

/* Hero risk banner */
.mirs-risk-hero {
    border-radius: var(--mirs-radius);
    padding: 1.75rem 2rem;
    text-align: center;
    margin: 1.25rem 0 1.5rem 0;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: var(--mirs-shadow), inset 0 1px 0 rgba(255, 255, 255, 0.06);
}

.mirs-risk-hero h1 {
    font-size: clamp(1.35rem, 3vw, 1.85rem);
    font-weight: 700;
    margin: 0 0 0.5rem 0;
    color: #fff;
    letter-spacing: 0.02em;
}

.mirs-risk-hero .mirs-risk-score {
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0.25rem 0;
    font-family: 'JetBrains Mono', monospace;
}

.mirs-risk-hero .mirs-risk-meta {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 1.5rem;
    margin-top: 1rem;
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.88);
}

/* Risk bar */
.mirs-risk-bar-wrap {
    background: #1e2633;
    height: 10px;
    border-radius: 999px;
    overflow: hidden;
    margin-top: 0.75rem;
}

.mirs-risk-bar-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.4s ease;
}

/* Tags */
.mirs-tag {
    display: inline-block;
    background: rgba(255, 71, 87, 0.18);
    color: #ff6b7a;
    border: 1px solid rgba(255, 71, 87, 0.35);
    padding: 0.35rem 0.75rem;
    border-radius: 8px;
    margin: 0.25rem 0.35rem 0.25rem 0;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    font-family: 'JetBrains Mono', monospace;
}

/* Propaganda signal chips */
.mirs-signal-chip {
    background: var(--mirs-surface-elevated);
    border: 1px solid rgba(255, 71, 87, 0.25);
    border-radius: var(--mirs-radius-sm);
    padding: 0.65rem 0.85rem;
    margin-bottom: 0.5rem;
    text-align: left;
}

.mirs-signal-chip .phrase {
    color: #ff6b7a;
    font-weight: 600;
    font-size: 0.88rem;
    margin-bottom: 0.25rem;
}

.mirs-signal-chip .explain {
    color: var(--mirs-muted);
    font-size: 0.75rem;
    line-height: 1.4;
}

/* Analyst panel */
.mirs-analyst-panel {
    background: linear-gradient(135deg, #111820 0%, #161d28 100%);
    padding: 1.5rem 1.65rem;
    border-radius: var(--mirs-radius);
    border: 1px solid var(--mirs-border);
    border-left: 4px solid var(--mirs-accent);
    box-shadow: var(--mirs-shadow), var(--mirs-glow);
    margin: 0.75rem 0 1rem 0;
}

.mirs-analyst-panel h3 {
    color: var(--mirs-accent);
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin: 0 0 0.85rem 0;
    font-family: 'JetBrains Mono', monospace;
}

.mirs-analyst-panel p {
    color: #c5d0de;
    font-size: 1rem;
    line-height: 1.75;
    margin: 0;
}

/* Highlighted article */
.mirs-highlight-panel {
    background: var(--mirs-surface);
    border: 1px solid var(--mirs-border);
    border-radius: var(--mirs-radius);
    padding: 1.25rem 1.5rem;
    max-height: 420px;
    overflow-y: auto;
    line-height: 1.85;
    font-size: 0.95rem;
    color: var(--mirs-text);
}

.mirs-highlight {
    background: linear-gradient(90deg, rgba(255, 71, 87, 0.28), rgba(255, 183, 3, 0.18));
    border-bottom: 2px solid #ff6b7a;
    padding: 1px 3px;
    border-radius: 3px;
    cursor: help;
    position: relative;
}

.mirs-highlight-tag {
    font-size: 0.6rem;
    color: #ff6b7a;
    margin-left: 1px;
    vertical-align: super;
}

.mirs-legend {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    font-size: 0.78rem;
    color: var(--mirs-muted);
    margin-bottom: 0.75rem;
}

.mirs-legend span {
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

.mirs-legend .swatch {
    width: 14px;
    height: 14px;
    border-radius: 3px;
    background: linear-gradient(90deg, rgba(255, 71, 87, 0.5), rgba(255, 183, 3, 0.35));
    border-bottom: 2px solid #ff6b7a;
}

/* Input panel */
.mirs-input-panel {
    background: var(--mirs-surface);
    border: 1px solid var(--mirs-border);
    border-radius: var(--mirs-radius);
    padding: 1.25rem 1.35rem 0.5rem 1.35rem;
    margin-bottom: 1rem;
}

/* Metric override inside cards */
div[data-testid="stMetric"] {
    background: transparent;
}

div[data-testid="stMetric"] label {
    color: var(--mirs-muted) !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

div[data-testid="stMetricValue"] {
    color: var(--mirs-text) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #0099cc 0%, #00d4ff 100%) !important;
    color: #0a0e14 !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: var(--mirs-radius-sm) !important;
    padding: 0.6rem 1.5rem !important;
    box-shadow: 0 4px 20px rgba(0, 212, 255, 0.25) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}

.stButton > button:hover {
    box-shadow: 0 6px 28px rgba(0, 212, 255, 0.35) !important;
    transform: translateY(-1px);
}

/* Dividers */
hr {
    border-color: var(--mirs-border) !important;
    margin: 1.5rem 0 !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--mirs-surface) !important;
    border-radius: var(--mirs-radius-sm) !important;
}

/* Progress bars */
.stProgress > div > div {
    background: linear-gradient(90deg, #0099cc, #00d4ff) !important;
}

.stProgress > div {
    background-color: #1e2633 !important;
    border-radius: 999px !important;
}

/* Disclaimer */
.mirs-disclaimer {
    font-size: 0.78rem;
    color: var(--mirs-muted);
    line-height: 1.5;
    padding: 0.75rem 0;
    border-top: 1px solid var(--mirs-border);
    margin-top: 1rem;
}
</style>
"""


def inject_theme():
    import streamlit as st

    st.markdown(THEME_CSS, unsafe_allow_html=True)

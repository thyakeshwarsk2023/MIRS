"""Interpretable narrative manipulation highlighting for article text."""

from src.propoganda import get_phrase_explanation


def _escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _merge_spans(spans: list[tuple[int, int, str]]) -> list[tuple[int, int, str]]:
    if not spans:
        return []

    ordered = sorted(spans, key=lambda x: (x[0], -(x[1] - x[0])))
    merged: list[tuple[int, int, str]] = [ordered[0]]

    for start, end, phrase in ordered[1:]:
        prev_start, prev_end, prev_phrase = merged[-1]
        if start <= prev_end:
            if end > prev_end:
                merged[-1] = (prev_start, end, prev_phrase)
        else:
            merged.append((start, end, phrase))

    return merged


def highlight_propaganda_text(text: str, matches: list[str]) -> str:
    """
    Wrap detected rhetorical phrases in annotated spans with analyst explanations.
    """
    if not text:
        return '<p class="mirs-article-body"></p>'

    if not matches:
        return f'<p class="mirs-article-body">{_escape_html(text)}</p>'

    text_lower = text.lower()
    spans: list[tuple[int, int, str]] = []

    for phrase in set(matches):
        phrase_lower = phrase.lower()
        search_from = 0
        while True:
            idx = text_lower.find(phrase_lower, search_from)
            if idx == -1:
                break
            spans.append((idx, idx + len(phrase), phrase))
            search_from = idx + 1

    merged = _merge_spans(spans)
    parts: list[str] = []
    cursor = 0

    for start, end, phrase in merged:
        parts.append(_escape_html(text[cursor:start]))
        snippet = _escape_html(text[start:end])
        explanation = _escape_html(get_phrase_explanation(phrase))
        label = _escape_html(phrase)
        parts.append(
            f'<span class="mirs-highlight" title="{explanation}" data-label="{label}">'
            f"{snippet}<sup class="mirs-highlight-tag">⚠</sup></span>"
        )
        cursor = end

    parts.append(_escape_html(text[cursor:]))
    body = "".join(parts)
    return f'<p class="mirs-article-body">{body}</p>'

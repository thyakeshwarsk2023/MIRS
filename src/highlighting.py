"""Interpretable narrative manipulation highlighting for article text."""

from src.propoganda import get_phrase_explanation


def _escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _merge_spans(spans: list) -> list:
    if not spans:
        return []

    ordered = sorted(spans, key=lambda x: (x[0], -(x[1] - x[0])))
    merged = [ordered[0]]

    for start, end, phrase in ordered[1:]:
        prev_start, prev_end, prev_phrase = merged[-1]
        if start <= prev_end:
            if end > prev_end:
                merged[-1] = (prev_start, end, prev_phrase)
        else:
            merged.append((start, end, phrase))

    return merged


def highlight_propaganda_text(text: str, matches: list) -> str:
    """
    Wrap detected rhetorical phrases in annotated spans with analyst explanations.
    """
    if not text:
        return '<p class="mirs-article-body"></p>'

    if not matches:
        return '<p class="mirs-article-body">' + _escape_html(text) + '</p>'

    text_lower = text.lower()
    spans = []

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
    parts = []
    cursor = 0

    for start, end, phrase in merged:
        parts.append(_escape_html(text[cursor:start]))
        snippet     = _escape_html(text[start:end])
        explanation = _escape_html(get_phrase_explanation(phrase))
        label       = _escape_html(phrase)

        # Build span without nesting quotes inside f-string
        parts.append(
            '<span class="mirs-highlight"'
            ' title="' + explanation + '"'
            ' data-label="' + label + '">'
            + snippet
            + '<sup class="mirs-highlight-tag">&#9888;</sup>'
            + '</span>'
        )
        cursor = end

    parts.append(_escape_html(text[cursor:]))
    body = "".join(parts)
    return '<p class="mirs-article-body">' + body + '</p>'
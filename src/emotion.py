from vaderSentiment.vaderSentiment import (
    SentimentIntensityAnalyzer
)

analyzer = SentimentIntensityAnalyzer()


def analyze_emotion(text):

    """
    Emotion & narrative pressure analysis
    using VADER sentiment scoring.

    Returns:
        emotion_type
        emotion_intensity
        negative_score
        neutral_score
        positive_score
    """

    # =====================================================
    # RAW SENTIMENT SCORES
    # =====================================================

    scores = analyzer.polarity_scores(text)

    compound = scores["compound"]

    negative_score = round(
        scores["neg"] * 100,
        2
    )

    neutral_score = round(
        scores["neu"] * 100,
        2
    )

    positive_score = round(
        scores["pos"] * 100,
        2
    )

    # =====================================================
    # EMOTIONAL INTENSITY
    # =====================================================

    """
    Measures how emotionally charged
    the narrative is regardless of direction.
    """

    emotion_intensity = round(
        abs(compound) * 100,
        2
    )

    # =====================================================
    # DOMINANT POLARITY
    # =====================================================

    """
    News articles are naturally neutral-heavy.

    We compare ONLY positive vs negative pressure.

    A polarity becomes dominant only if it
    meaningfully exceeds the opposite polarity.
    """

    DOMINANCE_MARGIN = 5

    if negative_score > (
        positive_score + DOMINANCE_MARGIN
    ):

        dominant = "negative"

    elif positive_score > (
        negative_score + DOMINANCE_MARGIN
    ):

        dominant = "positive"

    else:

        dominant = "mixed"

    # =====================================================
    # EMOTION CLASSIFICATION
    # =====================================================

    # -----------------------------------------------------
    # HIGH FEAR / STRONG NEGATIVE MANIPULATION
    # -----------------------------------------------------

    if (
        compound <= -0.60
        and dominant == "negative"
        and negative_score >= 18
    ):

        emotion_type = (
            "High Fear Manipulation"
        )

    # -----------------------------------------------------
    # NEGATIVE EMOTIONAL FRAMING
    # -----------------------------------------------------

    elif (
        compound <= -0.35
        and dominant == "negative"
    ):

        emotion_type = (
            "Negative Emotional Framing"
        )

    # -----------------------------------------------------
    # MILD NEGATIVE BIAS
    # -----------------------------------------------------

    elif compound <= -0.15:

        emotion_type = (
            "Mild Negative Bias"
        )

    # -----------------------------------------------------
    # HYPE / SENSATIONALISM
    # -----------------------------------------------------

    elif (
        compound >= 0.60
        and dominant == "positive"
        and positive_score >= 18
    ):

        emotion_type = (
            "Hype / Sensationalist Tone"
        )

    # -----------------------------------------------------
    # POSITIVE PERSUASIVE FRAMING
    # -----------------------------------------------------

    elif (
        compound >= 0.35
        and dominant == "positive"
    ):

        emotion_type = (
            "Persuasive Positive Tone"
        )

    # -----------------------------------------------------
    # MILD POSITIVE FRAMING
    # -----------------------------------------------------

    elif compound >= 0.15:

        emotion_type = (
            "Mild Positive Framing"
        )

    # -----------------------------------------------------
    # MIXED / LOW EMOTIONAL PRESSURE
    # -----------------------------------------------------

    else:

        if dominant == "mixed":

            emotion_type = (
                "Mixed Emotional Framing"
            )

        else:

            emotion_type = (
                "Low Emotional Bias"
            )

    # =====================================================
    # RETURN RESULT
    # =====================================================

    return {

        "emotion_type":
        emotion_type,

        "emotion_intensity":
        emotion_intensity,

        "negative_score":
        negative_score,

        "neutral_score":
        neutral_score,

        "positive_score":
        positive_score
    }
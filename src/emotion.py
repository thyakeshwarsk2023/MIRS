from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_emotion(text):

    scores = analyzer.polarity_scores(text)

    compound = scores['compound']

    negative_score = round(scores['neg'] * 100, 2)
    neutral_score = round(scores['neu'] * 100, 2)
    positive_score = round(scores['pos'] * 100, 2)

    emotion_intensity = round(abs(compound) * 100, 2)

    if compound <= -0.7:
        emotion_type = "High Fear Manipulation"

    elif compound <= -0.3:
        emotion_type = "Negative Emotional Framing"

    elif compound >= 0.7:
        emotion_type = "Hype/Manipulative Tone"

    elif compound >= 0.3:
        emotion_type = "Persuasive Emotional Tone"

    else:
        emotion_type = "Low Emotional Bias"

    return {
        "emotion_type": emotion_type,
        "emotion_intensity": emotion_intensity,
        "negative_score": negative_score,
        "neutral_score": neutral_score,
        "positive_score": positive_score
    }
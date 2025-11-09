
###########################################################################################

# backend/tools/sentiment_tool.py - Alternative sentiment tool using TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()

def sentiment_tool_fn(text: str) -> str:
    s = _analyzer.polarity_scores(text)
    compound = s.get("compound", 0.0)
    if compound >= 0.05:
        label = "🟢 Positive"
    elif compound <= -0.05:
        label = "🔴 Negative"
    else:
        label = "⚪ Neutral"
    return f"Sentiment: {label}. Scores: {s}"


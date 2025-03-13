from textblob import TextBlob

def analyze_sentiment(text):
    sentiment = TextBlob(text).sentiment.polarity
    if sentiment < -0.3:
        return "distressed"
    elif sentiment > 0.3:
        return "happy"
    return "neutral"


from textblob import TextBlob

def analyze_sentiment(text):
    """
    Analyze sentiment using TextBlob.
    Returns: 'positive', 'negative', or 'neutral'
    """
    analysis = TextBlob(text)
    # Get the polarity score (-1 to 1)
    polarity = analysis.sentiment.polarity
    
    if polarity > 0:
        return 'positive'
    elif polarity < 0:
        return 'negative'
    else:
        return 'neutral'


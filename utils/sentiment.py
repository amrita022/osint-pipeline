from textblob import TextBlob

def add_sentiment(records):
    """
    Adds sentiment analysis to each record
    Sentiment polarity ranges from -1 (negative) to +1 (positive)
    """
    analyzed = 0
    
    for record in records:
        try:
            text = record.get("text", "")
            
            if text and len(text.strip()) > 0:
                # Perform sentiment analysis
                blob = TextBlob(text)
                sentiment_score = blob.sentiment.polarity
                
                # Add sentiment to record
                record["sentiment"] = round(sentiment_score, 3)
                analyzed += 1
            else:
                record["sentiment"] = 0.0
        
        except Exception as e:
            # If sentiment analysis fails, default to neutral
            record["sentiment"] = 0.0
    
    print(f"✓ Analyzed sentiment for {analyzed} records")
    return records

def classify_sentiment(score):
    """
    Classifies sentiment score into categories
    """
    if score > 0.3:
        return "Positive"
    elif score < -0.3:
        return "Negative"
    else:
        return "Neutral"

def get_sentiment_stats(records):
    """
    Returns statistics about sentiment distribution
    """
    if not records:
        return {}
    
    sentiments = [r.get("sentiment", 0) for r in records]
    
    positive = sum(1 for s in sentiments if s > 0.3)
    negative = sum(1 for s in sentiments if s < -0.3)
    neutral = len(sentiments) - positive - negative
    
    avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
    
    return {
        "total": len(records),
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "average": round(avg_sentiment, 3)
    }

# Test function
if __name__ == "__main__":
    test_records = [
        {"text": "I love this amazing product! It's fantastic!"},
        {"text": "This is terrible and I hate it."},
        {"text": "The weather is okay today."}
    ]
    
    analyzed = add_sentiment(test_records)
    
    for record in analyzed:
        score = record["sentiment"]
        category = classify_sentiment(score)
        print(f"Text: {record['text'][:50]}")
        print(f"Sentiment: {score} ({category})\n")
    
    stats = get_sentiment_stats(analyzed)
    print(f"Statistics: {stats}")
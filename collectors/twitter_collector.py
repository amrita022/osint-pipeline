import tweepy
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

TWITTER_KEY = os.getenv("TWITTER_KEY")
TWITTER_SECRET = os.getenv("TWITTER_SECRET")
TWITTER_BEARER = os.getenv("TWITTER_BEARER")

def fetch_twitter(query="OSINT", count=20):
    """
    Fetches tweets from Twitter API v2
    """
    try:
        # Using Bearer Token for Twitter API v2
        client = tweepy.Client(bearer_token=TWITTER_BEARER)
        
        # Search recent tweets
        tweets = client.search_recent_tweets(
            query=query,
            max_results=min(count, 100),  # Max 100 per request
            tweet_fields=['created_at', 'author_id', 'text']
        )
        
        results = []
        
        if tweets.data:
            for tweet in tweets.data:
                results.append({
                    "platform": "twitter",
                    "user": str(tweet.author_id),
                    "timestamp": str(tweet.created_at),
                    "text": tweet.text,
                    "url": f"https://twitter.com/i/web/status/{tweet.id}"
                })
        
        print(f"✓ Collected {len(results)} tweets for query: {query}")
        return results
        
    except Exception as e:
        print(f"✗ Twitter Error: {str(e)}")
        return []

# Test function
if __name__ == "__main__":
    print("Testing Twitter Collector...")
    data = fetch_twitter("AI", 5)
    for item in data[:2]:
        print(item)
import praw
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

REDDIT_ID = os.getenv("REDDIT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")

def fetch_reddit(subreddit="technology", limit=20):
    """
    Fetches posts from a specified subreddit
    """
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_ID,
            client_secret=REDDIT_SECRET,
            user_agent="osint_lab_v1.0"
        )
        
        results = []
        
        for post in reddit.subreddit(subreddit).hot(limit=limit):
            # Combine title and selftext
            full_text = post.title
            if post.selftext:
                full_text += " " + post.selftext
            
            results.append({
                "platform": "reddit",
                "user": str(post.author) if post.author else "deleted",
                "timestamp": datetime.fromtimestamp(post.created_utc).isoformat(),
                "text": full_text,
                "url": f"https://reddit.com{post.permalink}"
            })
        
        print(f"✓ Collected {len(results)} Reddit posts from r/{subreddit}")
        return results
        
    except Exception as e:
        print(f"✗ Reddit Error: {str(e)}")
        return []

# Test function
if __name__ == "__main__":
    print("Testing Reddit Collector...")
    data = fetch_reddit("python", 5)
    for item in data[:2]:
        print(item)
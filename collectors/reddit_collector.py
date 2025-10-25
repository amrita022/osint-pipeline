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
        # Debug: Show what credentials we're using
        print(f"   Reddit ID: {REDDIT_ID[:5]}... (exists: {bool(REDDIT_ID)})")
        print(f"   Reddit Secret: {REDDIT_SECRET[:5]}... (exists: {bool(REDDIT_SECRET)})")
        
        if not REDDIT_ID or not REDDIT_SECRET:
            raise Exception("Reddit credentials not found in .env file")
        
        reddit = praw.Reddit(
            client_id=REDDIT_ID,
            client_secret=REDDIT_SECRET,
            user_agent="osint_lab_v1.0_by_amrita"  # More specific user agent
        )
        
        # Test authentication
        print(f"   Attempting to access r/{subreddit}...")
        
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
        print(f"   Full error type: {type(e).__name__}")
        
        # Show helpful error messages
        if "401" in str(e):
            print("   → Check that REDDIT_ID and REDDIT_SECRET are correct")
            print("   → Make sure there are no quotes or spaces in .env")
        
        return []

# Test function
if __name__ == "__main__":
    print("Testing Reddit Collector...")
    data = fetch_reddit("python", 5)
    for item in data[:2]:
        print(item)
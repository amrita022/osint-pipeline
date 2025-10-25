import praw

# Hardcode credentials to test (we'll remove this after testing)
reddit = praw.Reddit(
    client_id="dw5lFANRT2KzizLYDO6wCQ",
    client_secret="QuiRuRjqAhE-XoTWFqFTZL_QuRqpfQ",
    user_agent="OSINT_Lab_Test by /u/YourRedditUsername"  # CHANGE THIS to your actual Reddit username
)

# Test authentication
try:
    # Try to access a subreddit
    subreddit = reddit.subreddit("python")
    print(f"✓ Successfully connected to Reddit!")
    print(f"  Subreddit: {subreddit.display_name}")
    print(f"  Subscribers: {subreddit.subscribers}")
    
    # Try to get a post
    for post in subreddit.hot(limit=1):
        print(f"\n✓ Successfully fetched post:")
        print(f"  Title: {post.title}")
        print(f"  Author: {post.author}")
        
except Exception as e:
    print(f"✗ Error: {e}")
    print(f"  Error type: {type(e).__name__}")
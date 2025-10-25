from datetime import datetime

def fetch_twitter(query="OSINT", count=20):
    """
    Mock Twitter collector for demonstration when API is rate limited
    Returns sample data
    """
    print(f"⚠️  Using mock Twitter data (API rate limited)")
    
    sample_tweets = [
        f"Breaking: New developments in {query} technology are changing the industry",
        f"Excited to announce our new {query} initiative launching next week!",
        f"Just published an article about {query} - check it out!",
        f"Thoughts on the future of {query}? Let's discuss in the comments",
        f"Our team has been working on {query} solutions for months. Here's what we learned...",
        f"Hot take: {query} is more important now than ever before",
        f"{query} conference was amazing! Met so many incredible people",
        f"New blog post: Everything you need to know about {query}",
        f"Can't believe how much {query} has evolved in the past year",
        f"Looking for experts in {query} - DM me if interested!"
    ]
    
    results = []
    for i in range(min(count, len(sample_tweets))):
        results.append({
            "platform": "twitter",
            "user": f"user{i+1}",
            "timestamp": datetime.now().isoformat(),
            "text": sample_tweets[i],
            "url": f"https://twitter.com/user{i+1}/status/mock{i+1}"
        })
    
    return results
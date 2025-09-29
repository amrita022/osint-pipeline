import instaloader

def fetch_instagram(username="nasa", limit=5):
    """
    Fetches Instagram posts from a public profile
    Note: Instagram may rate limit or block. Use sparingly.
    """
    try:
        L = instaloader.Instaloader()
        
        # Get profile
        profile = instaloader.Profile.from_username(L.context, username)
        
        results = []
        count = 0
        
        for post in profile.get_posts():
            if count >= limit:
                break
            
            results.append({
                "platform": "instagram",
                "user": username,
                "timestamp": post.date.isoformat(),
                "text": post.caption if post.caption else "No caption",
                "url": f"https://www.instagram.com/p/{post.shortcode}/"
            })
            count += 1
        
        print(f"✓ Collected {len(results)} Instagram posts from @{username}")
        return results
        
    except Exception as e:
        print(f"✗ Instagram Error: {str(e)}")
        print("Note: Instagram often blocks automated access. This is expected.")
        return []

# Test function
if __name__ == "__main__":
    print("Testing Instagram Collector...")
    data = fetch_instagram("natgeo", 3)
    for item in data[:2]:
        print(item)
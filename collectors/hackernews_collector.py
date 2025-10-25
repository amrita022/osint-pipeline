import requests
from datetime import datetime

def fetch_hackernews(query="", limit=20):
    """
    Fetches stories from Hacker News API (no authentication needed!)
    """
    try:
        # Get top stories
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(url, timeout=10)
        story_ids = response.json()[:limit]
        
        results = []
        
        for story_id in story_ids:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story_response = requests.get(story_url, timeout=5)
            story = story_response.json()
            
            if story and story.get('title'):
                results.append({
                    "platform": "hackernews",
                    "user": story.get('by', 'unknown'),
                    "timestamp": datetime.fromtimestamp(story.get('time', 0)).isoformat(),
                    "text": story.get('title', '') + ' ' + story.get('text', ''),
                    "url": story.get('url', f"https://news.ycombinator.com/item?id={story_id}")
                })
        
        print(f"✓ Collected {len(results)} Hacker News stories")
        return results
        
    except Exception as e:
        print(f"✗ Hacker News Error: {str(e)}")
        return []
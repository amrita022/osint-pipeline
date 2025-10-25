import requests
from datetime import datetime

def fetch_devto(query="python", limit=20):
    """
    Fetches articles from Dev.to API (no authentication needed!)
    """
    try:
        url = f"https://dev.to/api/articles?tag={query}&per_page={limit}"
        
        response = requests.get(url, timeout=10)
        articles = response.json()
        
        results = []
        
        for article in articles[:limit]:
            results.append({
                "platform": "devto",
                "user": article.get('user', {}).get('username', 'unknown'),
                "timestamp": article.get('published_at', datetime.now().isoformat()),
                "text": article.get('title', '') + ' ' + article.get('description', ''),
                "url": article.get('url', '')
            })
        
        print(f"✓ Collected {len(results)} Dev.to articles")
        return results
        
    except Exception as e:
        print(f"✗ Dev.to Error: {str(e)}")
        return []
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

def fetch_quora(query="osint", limit=5):
    """
    Scrapes Quora search results with improved parsing
    """
    try:
        # Add more realistic headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
        url = f"https://www.quora.com/search?q={query.replace(' ', '+')}"
        
        # Add timeout
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"Quora returned status code: {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        
        # Try multiple selectors for Quora's dynamic structure
        questions = soup.find_all("div", class_="q-box")
        
        if not questions:
            # Try alternative selectors
            questions = soup.find_all("a", href=True)
            questions = [q for q in questions if "/search" not in q.get('href', '')][:limit]
        
        for i, q in enumerate(questions[:limit]):
            text = q.get_text(strip=True)
            if text and len(text) > 20:  # Minimum length filter
                results.append({
                    "platform": "quora",
                    "user": "quora_user",
                    "timestamp": datetime.now().isoformat(),
                    "text": text,
                    "url": url
                })
        
        print(f"✓ Collected {len(results)} Quora questions for query: {query}")
        return results
        
    except Exception as e:
        print(f"✗ Quora Error: {str(e)}")
        return []
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_quora(query="osint", limit=5):
    """
    Scrapes Quora search results (basic scraping - may not always work)
    """
    try:
        url = f"https://www.quora.com/search?q={query.replace(' ', '+')}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        results = []
        
        # Quora's structure changes often, this is a basic attempt
        questions = soup.find_all("span", class_="q-text")
        
        for i, q in enumerate(questions):
            if i >= limit:
                break
            
            text = q.get_text(strip=True)
            if text:
                results.append({
                    "platform": "quora",
                    "user": "anonymous",
                    "timestamp": datetime.now().isoformat(),
                    "text": text,
                    "url": url
                })
        
        print(f"✓ Collected {len(results)} Quora questions for query: {query}")
        return results
        
    except Exception as e:
        print(f"✗ Quora Error: {str(e)}")
        return []

# Test function
if __name__ == "__main__":
    print("Testing Quora Collector...")
    data = fetch_quora("programming", 3)
    for item in data[:2]:
        print(item)
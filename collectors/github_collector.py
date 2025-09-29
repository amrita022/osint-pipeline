from github import Github
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_github(query="osint", limit=10):
    """
    Searches GitHub repositories based on query
    """
    try:
        g = Github(GITHUB_TOKEN)
        
        # Search repositories
        repos = g.search_repositories(query=query, sort="stars", order="desc")
        
        results = []
        count = 0
        
        for repo in repos:
            if count >= limit:
                break
            
            results.append({
                "platform": "github",
                "user": repo.owner.login,
                "timestamp": repo.created_at.isoformat(),
                "text": f"{repo.name}: {repo.description or 'No description'}",
                "url": repo.html_url
            })
            count += 1
        
        print(f"✓ Collected {len(results)} GitHub repos for query: {query}")
        return results
        
    except Exception as e:
        print(f"✗ GitHub Error: {str(e)}")
        return []

# Test function
if __name__ == "__main__":
    print("Testing GitHub Collector...")
    data = fetch_github("python", 5)
    for item in data[:2]:
        print(item)
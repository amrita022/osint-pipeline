"""
Flask Web Dashboard for OSINT Pipeline
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

# Import your collectors
from collectors.twitter_collector import fetch_twitter
from collectors.reddit_collector import fetch_reddit
from collectors.github_collector import fetch_github
from collectors.instagram_collector import fetch_instagram
from collectors.quora_collector import fetch_quora

# Import utilities
from utils.cleaner import clean_text, filter_english
from utils.database import save_to_db, get_record_count
from utils.sentiment import add_sentiment

app = Flask(__name__)
CORS(app)

# Configuration
DATABASE_PATH = "data/osint.db"

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    """
    API endpoint to search and collect OSINT data
    """
    try:
        data = request.get_json()
        query = data.get('query', 'OSINT')
        
        if not query:
            return jsonify({'error': 'Query parameter required'}), 400
        
        print(f"🔍 Searching for: {query}")
        
        # Collect data from platforms
        collected_data = []
        
        # Twitter
        try:
            twitter_data = fetch_twitter(query, 5)
            collected_data.extend(twitter_data)
        except Exception as e:
            print(f"Twitter error: {e}")
        
        # Reddit
        try:
            reddit_data = fetch_reddit("technology", 5)
            collected_data.extend(reddit_data)
        except Exception as e:
            print(f"Reddit error: {e}")
        
        # GitHub
        try:
            github_data = fetch_github(query, 5)
            collected_data.extend(github_data)
        except Exception as e:
            print(f"GitHub error: {e}")
        
        # Instagram
        try:
            instagram_data = fetch_instagram("nasa", 3)
            collected_data.extend(instagram_data)
        except Exception as e:
            print(f"Instagram error: {e}")
        
        # Quora
        try:
            quora_data = fetch_quora(query, 3)
            collected_data.extend(quora_data)
        except Exception as e:
            print(f"Quora error: {e}")
        
        # Clean data
        for record in collected_data:
            if "text" in record:
                record["text"] = clean_text(record["text"])
        
        # Filter English
        collected_data = filter_english(collected_data)
        
        # Add sentiment
        collected_data = add_sentiment(collected_data)
        
        # Save to database
        save_to_db(collected_data)
        
        print(f"✅ Collected {len(collected_data)} records")
        
        return jsonify({
            'success': True,
            'count': len(collected_data),
            'data': collected_data,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/recent', methods=['GET'])
def get_recent():
    """
    Get recent posts from database
    """
    try:
        limit = request.args.get('limit', 20, type=int)
        
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        cur.execute("""
            SELECT * FROM osint_data 
            ORDER BY created_at DESC 
            LIMIT ?
        """, (limit,))
        
        rows = cur.fetchall()
        conn.close()
        
        # Convert to list of dicts
        results = []
        for row in rows:
            results.append({
                'id': row['id'],
                'platform': row['platform'],
                'user': row['user'],
                'timestamp': row['timestamp'],
                'text': row['text'],
                'url': row['url'],
                'sentiment': row['sentiment']
            })
        
        return jsonify({
            'success': True,
            'count': len(results),
            'data': results
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    Get database statistics
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cur = conn.cursor()
        
        # Total records
        cur.execute("SELECT COUNT(*) FROM osint_data")
        total = cur.fetchone()[0]
        
        # By platform
        cur.execute("""
            SELECT platform, COUNT(*) as count 
            FROM osint_data 
            GROUP BY platform
        """)
        by_platform = dict(cur.fetchall())
        
        # Average sentiment
        cur.execute("SELECT AVG(sentiment) FROM osint_data")
        avg_sentiment = cur.fetchone()[0] or 0
        
        conn.close()
        
        return jsonify({
            'success': True,
            'total_records': total,
            'by_platform': by_platform,
            'avg_sentiment': round(avg_sentiment, 3)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create data directory if not exists
    os.makedirs('data', exist_ok=True)
    
    print("\n" + "="*60)
    print("🌐 OSINT Pipeline Web Dashboard")
    print("="*60)
    print("📍 URL: http://127.0.0.1:5000")
    print("⚡ Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=8080)
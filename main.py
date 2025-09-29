"""
OSINT Social Media Aggregation Pipeline
Main entry point for automated data collection
"""

import sys
from datetime import datetime

# Import collectors
from collectors.twitter_collector import fetch_twitter
from collectors.reddit_collector import fetch_reddit
from collectors.github_collector import fetch_github
from collectors.instagram_collector import fetch_instagram
from collectors.quora_collector import fetch_quora

# Import utilities
from utils.cleaner import clean_text, filter_english
from utils.database import save_to_db, get_record_count
from utils.sentiment import add_sentiment, get_sentiment_stats
from utils.visualizer import create_all_visualizations

def print_banner():
    """Prints a welcome banner"""
    print("\n" + "="*60)
    print("     OSINT SOCIAL MEDIA AGGREGATION PIPELINE")
    print("     Fr. Conceicao Rodrigues College of Engineering")
    print("="*60 + "\n")

def run_pipeline(query="OSINT", collect_count=10):
    """
    Main pipeline function that orchestrates the entire OSINT collection
    """
    print_banner()
    print(f"🚀 Starting OSINT collection for query: '{query}'")
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Step 1: Collect data from multiple platforms
    print("📥 STEP 1: Collecting data from social media platforms...\n")
    
    all_data = []
    
    # Twitter
    try:
        twitter_data = fetch_twitter(query, collect_count)
        all_data.extend(twitter_data)
    except Exception as e:
        print(f"⚠️  Twitter collection failed: {str(e)}")
    
    # Reddit
    try:
        reddit_data = fetch_reddit("technology", collect_count)
        all_data.extend(reddit_data)
    except Exception as e:
        print(f"⚠️  Reddit collection failed: {str(e)}")
    
    # GitHub
    try:
        github_data = fetch_github(query, collect_count)
        all_data.extend(github_data)
    except Exception as e:
        print(f"⚠️  GitHub collection failed: {str(e)}")
    
    # Instagram (may fail due to rate limiting)
    try:
        instagram_data = fetch_instagram("nasa", 5)
        all_data.extend(instagram_data)
    except Exception as e:
        print(f"⚠️  Instagram collection failed: {str(e)}")
    
    # Quora
    try:
        quora_data = fetch_quora(query, 5)
        all_data.extend(quora_data)
    except Exception as e:
        print(f"⚠️  Quora collection failed: {str(e)}")
    
    print(f"\n✅ Total raw records collected: {len(all_data)}\n")
    
    if len(all_data) == 0:
        print("❌ No data collected. Check your API keys and internet connection.")
        return False
    
    # Step 2: Clean the data
    print("🧹 STEP 2: Cleaning and preprocessing data...\n")
    
    for record in all_data:
        if "text" in record:
            record["text"] = clean_text(record["text"])
    
    # Filter for English content only
    all_data = filter_english(all_data)
    
    print(f"✅ Records after cleaning: {len(all_data)}\n")
    
    # Step 3: Sentiment Analysis
    print("😊 STEP 3: Performing sentiment analysis...\n")
    
    all_data = add_sentiment(all_data)
    
    # Show sentiment statistics
    stats = get_sentiment_stats(all_data)
    print(f"\n📊 Sentiment Statistics:")
    print(f"   Total records: {stats['total']}")
    print(f"   Positive: {stats['positive']} ({stats['positive']/stats['total']*100:.1f}%)")
    print(f"   Neutral: {stats['neutral']} ({stats['neutral']/stats['total']*100:.1f}%)")
    print(f"   Negative: {stats['negative']} ({stats['negative']/stats['total']*100:.1f}%)")
    print(f"   Average sentiment: {stats['average']}")
    
    # Step 4: Save to database
    print("\n💾 STEP 4: Saving to database...\n")
    
    saved_count = save_to_db(all_data)
    total_records = get_record_count()
    
    print(f"✅ Database now contains {total_records} total records\n")
    
    # Step 5: Create visualizations
    print("📈 STEP 5: Creating visualizations...\n")
    
    create_all_visualizations()
    
    # Final summary
    print("\n" + "="*60)
    print("✅ PIPELINE COMPLETED SUCCESSFULLY!")
    print("="*60)
    print(f"\n📊 Summary:")
    print(f"   • Records collected this run: {len(all_data)}")
    print(f"   • Total records in database: {total_records}")
    print(f"   • Database location: data/osint.db")
    print(f"   • Screenshots saved in: screenshots/")
    print("\n" + "="*60 + "\n")
    
    return True

def main():
    """
    Main entry point with user options
    """
    if len(sys.argv) > 1:
        query = sys.argv[1]
    else:
        query = "AI"  # Default query
    
    try:
        success = run_pipeline(query=query, collect_count=15)
        
        if success:
            print("✅ Pipeline executed successfully!")
            print("📁 Check the 'data' folder for osint.db")
            print("📸 Check the 'screenshots' folder for visualizations")
        else:
            print("❌ Pipeline encountered errors. Check the logs above.")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Pipeline interrupted by user. Exiting...")
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
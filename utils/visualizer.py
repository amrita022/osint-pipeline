import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
import os

def plot_sentiment_by_platform(db_path="data/osint.db", save_path="screenshots/sentiment_by_platform.png"):
    """
    Creates a bar chart showing average sentiment by platform
    """
    try:
        # Read data from database
        conn = sqlite3.connect(db_path)
        df = pd.read_sql("SELECT platform, sentiment FROM osint_data", conn)
        conn.close()
        
        if df.empty:
            print("No data to visualize")
            return False
        
        # Calculate average sentiment by platform
        avg_sentiment = df.groupby("platform")["sentiment"].mean().sort_values()
        
        # Create plot
        plt.figure(figsize=(10, 6))
        avg_sentiment.plot(kind="bar", color=['red' if x < 0 else 'green' for x in avg_sentiment])
        plt.title("Average Sentiment by Platform", fontsize=16, fontweight='bold')
        plt.xlabel("Platform", fontsize=12)
        plt.ylabel("Average Sentiment Score", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
        plt.tight_layout()
        
        # Save plot
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved sentiment chart to {save_path}")
        plt.close()
        
        return True
        
    except Exception as e:
        print(f"✗ Visualization Error: {str(e)}")
        return False

def plot_post_count_by_platform(db_path="data/osint.db", save_path="screenshots/post_count.png"):
    """
    Creates a bar chart showing number of posts collected per platform
    """
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql("SELECT platform FROM osint_data", conn)
        conn.close()
        
        if df.empty:
            print("No data to visualize")
            return False
        
        # Count posts by platform
        counts = df["platform"].value_counts().sort_values(ascending=False)
        
        # Create plot
        plt.figure(figsize=(10, 6))
        counts.plot(kind="bar", color='steelblue')
        plt.title("Number of Posts Collected by Platform", fontsize=16, fontweight='bold')
        plt.xlabel("Platform", fontsize=12)
        plt.ylabel("Number of Posts", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Save plot
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved post count chart to {save_path}")
        plt.close()
        
        return True
        
    except Exception as e:
        print(f"✗ Visualization Error: {str(e)}")
        return False

def plot_sentiment_distribution(db_path="data/osint.db", save_path="screenshots/sentiment_distribution.png"):
    """
    Creates a histogram showing distribution of sentiment scores
    """
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql("SELECT sentiment FROM osint_data", conn)
        conn.close()
        
        if df.empty:
            print("No data to visualize")
            return False
        
        # Create histogram
        plt.figure(figsize=(10, 6))
        plt.hist(df["sentiment"], bins=30, color='purple', alpha=0.7, edgecolor='black')
        plt.title("Distribution of Sentiment Scores", fontsize=16, fontweight='bold')
        plt.xlabel("Sentiment Score", fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        plt.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Neutral')
        plt.legend()
        plt.tight_layout()
        
        # Save plot
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved sentiment distribution to {save_path}")
        plt.close()
        
        return True
        
    except Exception as e:
        print(f"✗ Visualization Error: {str(e)}")
        return False

def create_all_visualizations(db_path="data/osint.db"):
    """
    Creates all visualization charts
    """
    print("\n📊 Creating visualizations...")
    plot_sentiment_by_platform(db_path)
    plot_post_count_by_platform(db_path)
    plot_sentiment_distribution(db_path)
    print("✓ All visualizations created!\n")

# Test function
if __name__ == "__main__":
    print("Testing visualizer...")
    create_all_visualizations()
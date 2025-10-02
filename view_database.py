import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("data/osint.db")

# Read all data
df = pd.read_sql("SELECT * FROM osint_data", conn)

# Display info
print("\n" + "="*80)
print("DATABASE CONTENTS")
print("="*80)
print(f"\nTotal records: {len(df)}")
print(f"\nPlatforms: {df['platform'].value_counts().to_dict()}")
print(f"\n{'='*80}")
print("\nFirst 10 records:")
print("="*80)

# Show first 10 records nicely
for i, (_, row) in enumerate(df.head(10).iterrows(), start=1):
    print(f"\nRecord {i}:")
    print(f"  Platform: {row['platform']}")
    print(f"  User: {row['user']}")
    print(f"  Timestamp: {row['timestamp']}")
    print(f"  Text: {row['text'][:100]}...")
    print(f"  Sentiment: {row['sentiment']}")
    print(f"  URL: {row['url']}")
    print("-" * 80)

conn.close()

print("\n✅ Database query complete!\n")
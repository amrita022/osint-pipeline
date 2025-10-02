"""
Automated scheduler for OSINT pipeline
Runs the pipeline every hour
"""

import schedule
import time
from datetime import datetime
from main import run_pipeline

def scheduled_job():
    """
    Function that runs on schedule
    """
    print("\n" + "="*60)
    print(f"⏰ SCHEDULED RUN at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")
    
    run_pipeline(query="OSINT", collect_count=10)

# Schedule the job every 1 hour
schedule.every(1).hours.do(scheduled_job)

print("\n" + "="*60)
print("🤖 OSINT PIPELINE SCHEDULER STARTED")
print("="*60)
print(f"⏰ Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("📅 Schedule: Every 1 hour")
print("⚠️  Press Ctrl+C to stop the scheduler")
print("="*60 + "\n")

# Run once immediately
print("▶️  Running initial collection...")
scheduled_job()

# Keep the script running
print("\n⏳ Waiting for next scheduled run...")
print("   Next run in: 1 hour\n")

try:
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute
except KeyboardInterrupt:
    print("\n\n⚠️  Scheduler stopped by user. Goodbye!")
    print("="*60 + "\n")
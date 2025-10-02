# OSINT Social Media Aggregation Pipeline

An automated Python pipeline for collecting, processing, and analyzing social media data from multiple platforms for Open Source Intelligence (OSINT) purposes.

## Overview

This project implements a modular OSINT collection system that aggregates data from Twitter, Reddit, GitHub, Instagram, and Quora. The pipeline performs automated text cleaning, language detection, sentiment analysis, and data visualization.

## Features

- Multi-platform data collection (Twitter, Reddit, GitHub, Instagram, Quora)
- Automated text preprocessing and language filtering
- Sentiment analysis using TextBlob
- SQLite database storage with structured schema
- Automated visualization generation
- Configurable task scheduling
- Modular architecture for easy extensibility

## Requirements

- Python 3.9+
- API credentials for target platforms
- Required Python packages (see `requirements.txt`)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/osint-pipeline.git
cd osint-pipeline

# Create virtual environment
python -m venv osint_env
source osint_env/bin/activate  # On Windows: osint_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with your API credentials:

```env
TWITTER_KEY=your_twitter_api_key
TWITTER_SECRET=your_twitter_secret
TWITTER_BEARER=your_bearer_token

REDDIT_ID=your_reddit_client_id
REDDIT_SECRET=your_reddit_secret

GITHUB_TOKEN=your_github_token
```

### Obtaining API Keys

- **Twitter:** https://developer.twitter.com/
- **Reddit:** https://www.reddit.com/prefs/apps
- **GitHub:** https://github.com/settings/tokens

## Usage

### Basic Collection

```bash
# Run single collection with default query
python main.py

# Run with custom search term
python main.py "cybersecurity"
```

### View Database

```bash
python view_database.py
```

### Automated Scheduling

```bash
# Run continuous collection every hour
python scheduler.py
```

## Project Structure

```
osint_pipeline/
├── collectors/          # Platform-specific data collectors
│   ├── twitter_collector.py
│   ├── reddit_collector.py
│   ├── github_collector.py
│   └── ...
├── utils/              # Utility modules
│   ├── cleaner.py     # Text preprocessing
│   ├── database.py    # Database operations
│   ├── sentiment.py   # Sentiment analysis
│   └── visualizer.py  # Chart generation
├── data/              # Data storage
│   └── osint.db      # SQLite database
├── main.py           # Main pipeline
├── scheduler.py      # Automation scheduler
└── requirements.txt  # Dependencies
```

## Database Schema

The SQLite database (`data/osint.db`) uses the following schema:

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| platform | TEXT | Source platform |
| user | TEXT | Username/author |
| timestamp | TEXT | Post creation time |
| text | TEXT | Post content (cleaned) |
| url | TEXT | Post URL |
| sentiment | REAL | Sentiment score (-1 to 1) |
| created_at | DATETIME | Record creation time |

## Output

The pipeline generates:
- SQLite database with collected records
- Sentiment analysis visualizations (bar charts, histograms)
- Platform distribution charts
- CSV exports (optional)

## Architecture

The system follows a modular design pattern:

1. **Collection Layer:** Platform-specific collectors using official APIs
2. **Processing Layer:** Text cleaning, language detection, sentiment analysis
3. **Storage Layer:** SQLite database with normalized schema
4. **Visualization Layer:** Matplotlib-based chart generation
5. **Automation Layer:** Schedule-based continuous monitoring

## Technical Stack

- **Core:** Python 3.9+
- **APIs:** tweepy, praw, PyGithub, instaloader
- **Data Processing:** pandas, numpy, langdetect, textblob
- **Storage:** SQLite3
- **Visualization:** matplotlib
- **Automation:** schedule

## Limitations

- API rate limits apply (varies by platform)
- Instagram access is restricted and may fail frequently
- Some platforms require authenticated access
- Language detection requires minimum text length
- Real-time streaming not implemented

## License

This project is developed for educational purposes. Users must comply with the Terms of Service of all integrated platforms.

## Acknowledgments

Developed as part of the OSINT & Threat Intelligence Lab curriculum at Fr. Conceicao Rodrigues College of Engineering, Department of Computer Engineering.

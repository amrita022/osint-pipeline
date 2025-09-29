import re
from langdetect import detect, LangDetectException

def clean_text(text):
    """
    Cleans text by removing URLs, special characters, extra spaces
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text

def filter_english(records):
    """
    Filters records to keep only English language content
    """
    english_records = []
    
    for record in records:
        try:
            text = record.get("text", "")
            
            # Skip empty text
            if not text or len(text.strip()) < 10:
                continue
            
            # Detect language
            lang = detect(text)
            
            if lang == "en":
                english_records.append(record)
        
        except LangDetectException:
            # If language detection fails, skip
            continue
        except Exception as e:
            # Skip problematic records
            continue
    
    print(f"✓ Filtered to {len(english_records)} English records from {len(records)} total")
    return english_records

# Test function
if __name__ == "__main__":
    test_text = "Check out this link: https://example.com and email me@test.com !!!"
    cleaned = clean_text(test_text)
    print(f"Original: {test_text}")
    print(f"Cleaned: {cleaned}")
    
    test_records = [
        {"text": "This is English text"},
        {"text": "Esto es español"},
        {"text": "Another English sentence"}
    ]
    filtered = filter_english(test_records)
    print(f"\nFiltered {len(filtered)} English records")
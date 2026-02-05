import re
import pandas as pd
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")


"""
Text Preprocessing Module

Provides utilities to clean and standardise raw text prior to
sentiment analysis

The cleaning process:

- Converts text to lowercase
- Removes URLs, users, subreddit references, HTML artifacts
- Filters non-essential characters while preserving punctuation
- Removes common English stopwords
- Normalises whitespace

Future consideration for language, Manchester united has a global following
so look to incorporate feedback in languages other than english


"""

STOP_WORDS = set(stopwords.words("english"))

def clean_text(text: str) -> str:
    if not text or pd.isna(text):
        return ""

    text = text.lower()

    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"@\w+|u/\w+|r/\w+", "", text)
    text = re.sub(r"&\w+;", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s!?.,]", "", text)

    text = " ".join(
        word for word in text.split()
        if word not in STOP_WORDS
    )

    return re.sub(r"\s+", " ", text).strip()
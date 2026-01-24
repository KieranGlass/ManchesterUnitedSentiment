import requests
import feedparser
from pathlib import Path
import pandas as pd
from datetime import datetime
from src.preprocessing import clean_text

MANCHESTER_UNITED_KEYWORDS = [
    "man united",
    "mufc",
    "the red devils",
    "manchester united",
    "old trafford"
]

def fetch_reddit_json(subreddits, mu_only, limit=50):
    url_template = "https://www.reddit.com/r/{}/new.json"
    headers = {"User-Agent": "manchester-united-sentiment-uni-project"}

    Path("data/reddit").mkdir(parents=True, exist_ok=True)
    all_posts = []

    for subreddit in subreddits:
        url = url_template.format(subreddit)
        params = {"limit": limit}

        r = requests.get(url, headers=headers, params=params, timeout=10)
        r.raise_for_status()

        posts = r.json()["data"]["children"]

        for post in posts:
            p = post["data"]

            raw_title = p.get("title", "").strip()
            if not raw_title:
                continue

            text_lower = raw_title.lower()

            if mu_only:
                include = True
            else:
                include = any(keyword in text_lower for keyword in MANCHESTER_UNITED_KEYWORDS)

            if not include:
                continue

            cleaned = clean_text(raw_title)
            if not cleaned:
                continue

            all_posts.append({
                "date": datetime.utcfromtimestamp(p["created_utc"]).strftime("%Y-%m-%d"),
                "text": cleaned,
                "source": f"r/{subreddit}"
            })

    df = pd.DataFrame(all_posts)

    output_file = (
        "data/reddit/mu_posts.csv"
        if mu_only
        else "data/reddit/general_posts.csv"
    )

    df.to_csv(output_file, index=False, encoding="utf-8")

    return len(df)


def fetch_news_rss(feeds, mu_only, limit_per_feed=50):
    Path("data/news").mkdir(parents=True, exist_ok=True)
    all_articles = []

    for feed_url in feeds:
        
        feed = feedparser.parse(feed_url)
        source_name = normalise_source(feed)
        
        for entry in feed.entries[:limit_per_feed]:
            
            text = f"{entry.title} {entry.summary}".lower()
            
            if any(keyword in text for keyword in MANCHESTER_UNITED_KEYWORDS):
                
                cleaned = clean_text(entry.title)
                
                if cleaned:
                    all_articles.append({
                        "date": datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d"),
                        "text": cleaned,
                        "source": source_name
                    })

    df = pd.DataFrame(all_articles)
    
    output_file = ""
        
    if mu_only:
        
        output_file = "data/news/mu_articles.csv"
    
    else: 
        
        output_file = "data/news/general_articles.csv"
    
    
    df.to_csv(output_file, index=False, encoding="utf-8")
    
    sources = sorted(df["source"].unique())
    return len(df), sources


def normalise_source(feed):
    
    title = feed.feed.get("title", "unknown").lower()

    if "bbc" in title:
        return "BBC Sport"
    if "guardian" in title:
        return "The Guardian"
    if "sky" in title:
        return "Sky News"
    if "manutd" in title or "manchester united" in title:
        return "Man United Official"
    if "espn" in title or "ESPN" in title:
        return "ESPN"

    return title.title()
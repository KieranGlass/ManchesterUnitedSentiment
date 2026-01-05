import requests
import feedparser
from pathlib import Path
import pandas as pd
from datetime import datetime

MANCHESTER_UNITED_KEYWORDS = [
    "man united",
    "mufc",
    "the red devils",
    "manchester united",
    "old trafford"
]

def fetch_reddit_json(subreddits, limit=50):
    url_template = "https://www.reddit.com/r/{}/new.json"
    headers = {"User-Agent": "bristol-city-sentiment-uni-project"}
    
    Path("data/reddit").mkdir(parents=True, exist_ok=True)
    total_rows = 0

    for subreddit in subreddits:
        rows = []
        
        url = url_template.format(subreddit)
        params = {"limit": limit}

        r = requests.get(url, headers=headers, params=params, timeout=10)
        r.raise_for_status()

        posts = r.json()["data"]["children"]
    
        for post in posts:
            p = post["data"]
            title = p['title'].strip()
            title_lower = title.lower()
            
            if subreddit.lower() in ["manchesterunited", "reddevils"]:
                include = True
            else:
                include = any(keyword in title_lower for keyword in MANCHESTER_UNITED_KEYWORDS)
            
            if include and title:
                rows.append({
                    "date": datetime.utcfromtimestamp(p["created_utc"]).strftime("%Y-%m-%d"),
                    "text": title
                })

        df = pd.DataFrame(rows)
        df.to_csv(
            f"data/reddit/{subreddit.lower()}_posts.csv",
            index=False,
            encoding="utf-8"
        )
        
        total_rows += len(df)

    return total_rows


def fetch_news_rss(feed_url="https://www.bbc.co.uk/sport/football/rss.xml", limit=10):
    feed = feedparser.parse(feed_url)
    data = []

    for entry in feed.entries[:limit]:
        data.append({
            "date": datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d"),
            "text": entry.title + " " + entry.summary
        })

    df = pd.DataFrame(data)
    df.to_csv("data/news/articles.csv", index=False)
    return df
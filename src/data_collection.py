from tkinter import messagebox
import requests
import feedparser
from pathlib import Path
import pandas as pd
from datetime import datetime
from src.preprocessing import clean_text

"""
Data Collection Module

This module is responsible for retrieving Manchester United related
text data from external sources and preparing it for sentiment analysis

Data is collected from (for now):

• Reddit — via Reddits JSON API, pulling hot posts from selected subreddits  
• News feeds — via RSS feeds from football and Manchester United sources

General Reddit and RSS News feeds are filtered using Man united keywords
constant variable - Future implementation could look to access these words
programmatically, especially as keywords change over time

Once data is collected it is prepared using utility from preprocessing.py

Standardised with date, text, and source metadata

The collected data is saved as CSV files in data folder for downstream
sentiment analysis and visualisation

The module also tracks per-source counts to support reporting
and transparency in the GUI and has a normalisation method for cleaning 
up sources when presented to user

Note: Subreddit limits placed at 100 and can easily be changed. also, reddit
thread comments allow a much deeper dive into sentiment. However both the limit
and comment functionality would require API calls that surpass what is allowed 
without a Reddit developer account and therefore wasnt continued with for now.

It is for that reason there are commented out fetch comments functionality in
this file  
"""

MU_SUBREDDITS = ["ManchesterUnited", "RedDevils"]
GENERAL_SUBREDDITS = ["soccer", "PremierLeague", "football"]

MU_NEWS_FEEDS = [
    "https://www.manutd.com/Feeds/NewsSecondRSSFeed",
    "https://thepeoplesperson.com/feed/",
    "https://therepublikofmancunia.com/feed/",
    "https://strettynews.com/feed/",
    "https://manutdnews.com/feed/",
]

GENERAL_NEWS_FEEDS = [
    "https://www.bbc.co.uk/sport/football/rss.xml",
    "https://www.101greatgoals.com/feed/",
    "https://www.espn.com/espn/rss/news",
    "https://www.theguardian.com/football/manchester-united/rss",
    "https://www.dailymail.co.uk/sport/manchester-united/articles.rss",
    "https://www.fourfourtwo.com/feeds.xml",
    "https://talksport.com/feed/",
    "https://www.skysports.com/rss/12040",
    "https://www.caughtoffside.com/tags/premier-league/feed/",
    "https://www.soccernews.com/category/english-premier-league/feed/",
    "https://feeds.bleacherreport.com/articles",
    "https://www.football365.com/manchester-united/rss2",
    "https://www.manchestereveningnews.co.uk/all-about/manchester-united-fc?service=rss",
    "https://www.si.com/feed",
    "https://www.footballfancast.com/feed",
    "https://metro.co.uk/tag/premier-league/feed",
    "https://football-talk.co.uk/topics/premier-league/feed",
    "https://e00-marca.uecdn.es/rss/en/football/premier-league.xml",
    "https://givemesport.com/premier-league/feed",
    "https://www.standard.co.uk/sport/rss",
    "https://www.independent.co.uk/sport/rss",
    "https://www.telegraph.co.uk/sport/rss.xml",
    "https://www.mirror.co.uk/sport/rss.xml",
    "https://news.google.com/rss/search?q=Manchester+United",
    
    
]

MANCHESTER_UNITED_KEYWORDS = [
    "man united", "mufc", "the red devils", "red devils", "manchester united", "manchester utd",
    "man u", "old trafford", "man utd", "bruno fernandes", "lisandro martinez", "harry maguire",
    "luke shaw", "matheus cunha", "stretford end", "casemiro", "sesko", "mbeumo", "amad diallo",
    "mason mount", "carrick", "ratcliffe", "jason wilcox", "omar berrada", "class of 92",
    "alex ferguson", "glazers", "senne lammens", "leny yoro", "darren fletcher", "dorgu",
    "paul scholes", "roy keane", "gary neville", "andy mitten", "ugarte", "kobbie mainoo"
]

def fetch_reddit_json(type, mu_only, limit=100):
    subreddits = []
    if type == "mu":
        subreddits = MU_SUBREDDITS
    elif type == "gen":
        subreddits = GENERAL_SUBREDDITS
    else:
        messagebox.showerror("error")
    
    url_template = "https://www.reddit.com/r/{}/hot.json"
    headers = {"User-Agent": "windows:manchester-united-sentiment-uni-project:v1.0"}

    Path("data/reddit").mkdir(parents=True, exist_ok=True)
    all_posts = []
    
    source_counts = {}

    for subreddit in subreddits:
        subreddit_posts = []
        title_count = 0
        after = None
        
        max_pages = 20
        pages = 0
        
        while title_count < limit and pages < max_pages:
            params = {
                "limit": 100,
                "after": after
            }
            
            url = url_template.format(subreddit)
            r = requests.get(url, headers=headers, params=params, timeout=10)
            r.raise_for_status()

            data = r.json()["data"]
            posts = data["children"]
            after = data["after"]
        
            print(subreddit, len(posts))
            
            if not posts:
                break 

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

                subreddit_posts.append({
                    "date": datetime.fromtimestamp(p["created_utc"]).strftime("%Y-%m-%d"),
                    "text": cleaned,
                    "source": f"r/{subreddit}",
                })
                
                title_count += 1
                
                # comments = fetch_comments(post_id)

                # for c in comments:
                    # subreddit_posts.append({
                        # "date": datetime.utcfromtimestamp(p["created_utc"]).strftime("%Y-%m-%d"),
                        # "text": c["text"],
                        # "source": f"r/{subreddit}",
                        # "level": "comment",
                        # "depth": c["depth"],
                        # "score": c["score"],
                        # "thread_id": post_id
                    # })
                
                if title_count >= limit:
                    break
                
            pages += 1
            
            if after is None:
                break  # reached end of subreddit history

        all_posts.extend(subreddit_posts)
        
        source_counts[f"r/{subreddit}"] = len(subreddit_posts)

    df = pd.DataFrame(all_posts)

    output_file = (
        "data/reddit/mu_posts.csv"
        if mu_only
        else "data/reddit/general_posts.csv"
    )

    df.to_csv(output_file, index=False, encoding="utf-8")

    return len(df), source_counts



"""
def fetch_comments(post_id, max_comments=5):
    
    url = f"https://www.reddit.com/comments/{post_id}.json?limit={max_comments}"
    headers = {"User-Agent": "windows:manchester-united-sentiment-uni-project:v1.0"}

    try:
        r = requests.get(url, headers=headers, timeout=5)
        r.raise_for_status()
        
    except requests.RequestException:
        return []

    data = r.json()
    
    if not isinstance(data, list) or len(data) < 2:
        return []

    comments_data = data[1]["data"]["children"]

    comments = []

    for c in comments_data:

        if c.get("kind") != "t1":
            continue

        d = c["data"]
        body = d.get("body", "").strip()
        if not body:
            continue

        cleaned = clean_text(body)
        if not cleaned:
            continue

        comments.append({
            "text": cleaned,
            "level": "comment",
            "depth": d.get("depth", 1),
            "score": d.get("score", 0)
        })

        if len(comments) >= max_comments:
            break

    return comments
"""

def fetch_news_rss(type, mu_only, limit_per_feed=50):
    feeds = []
    
    if type == "mu":
        feeds = MU_NEWS_FEEDS
    elif type == "gen":
        feeds = GENERAL_NEWS_FEEDS
    else:
        messagebox.showerror("error")
    
    Path("data/news").mkdir(parents=True, exist_ok=True)
    all_articles = []
    
    source_counts = {}

    for feed_url in feeds:
        
        feed = feedparser.parse(feed_url)
        source_name = normalise_source(feed)
        print(f"\nFeed: {feed_url} -> {len(feed.entries)} entries, source: {source_name}")
        
        for entry in feed.entries[:limit_per_feed]:
            
            text = get_entry_text(entry)
            
            if mu_only:
                include = True
            else:
                include = any(keyword in text for keyword in MANCHESTER_UNITED_KEYWORDS)
            if not include:
                print(f"    Skipped (no keyword match)")
                continue
                
            cleaned = clean_text(entry.title)
                
            if cleaned:
                all_articles.append({
                    "date": datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d"),
                    "text": cleaned,
                    "source": source_name
                })
                print(f"    Added: '{cleaned[:50]}...'")
                
                source_counts[source_name] = source_counts.get(source_name, 0) + 1

    df = pd.DataFrame(all_articles)
    
    output_file = ""
        
    if mu_only:
        
        output_file = "data/news/mu_articles.csv"
    
    else: 
        
        output_file = "data/news/general_articles.csv"
    
    
    df.to_csv(output_file, index=False, encoding="utf-8")
    
    
    return len(df), source_counts

def get_entry_text(entry):
    parts = []

    for attr in ["title", "summary", "description"]: # Can add "content" here to add articles that reference a keyword in the main content
        value = getattr(entry, attr, "")
        
        if isinstance(value, str):
            parts.append(value)
        elif isinstance(value, list):
            
            for item in value:
                if isinstance(item, dict) and "value" in item:
                    parts.append(item["value"])
    
    return " ".join(parts).lower()


def normalise_source(feed):
    
    # this is just about tidying up the about info after analysis is run for user
    
    title = feed.feed.get("title", "unknown").lower()

    if "bbc" in title:
        return "BBC Sport"
    if "guardian" in title:
        return "The Guardian"
    if "mail online" in title:
        return "The Daily Mail"
    if "sky" in title:
        return "Sky News"
    if "fourfourtwo" in title:
        return "Fourfourtwo"
    if "espn" in title or "ESPN" in title:
        return "ESPN"
    if "caughtoffside" in title:
        return "Caught Offside"
    if "metro" in title:
        return "Metro UK"
    if "marca" in title:
        return "Marca"
    if "mirror" in title:
        return "The Daily Mirror"
    if "standard" in title:
        return "London Evening Standard"
    if "independent" in title:
        return "The Independent"
    if "google news" in title:
        return "Google News"
    if "premiership results & table" in title:
        return "Soccer News"
    if "the latest news, gossip and transfer rumours" in title:
        return "Football-talk.co.uk"
    if "men - manchester united fc" in title:
        return "Manchester Evening News"
    if "football365.com | manchester united" in title:
        return "Football 365"
    if "givemesport" in title:
        return "Give Me Sport"
    if "the peoples person" in title:
        return "The Peoples Person"
    if "republik of mancunia" in title:
        return "Republik of Mancunia"
    if "stretty news" in title:
        return "Stretty News"
    if "manutd.com news rss" in title:
        return "ManUnited.com"
        
 
    return title.title()
import tkinter as tk
from tkinter import ttk
from src import data_collection, donut_chart, sentiment_analysis, styles
from tkinter import messagebox
from PIL import Image, ImageTk


# Subreddit groups
MU_SUBREDDITS = ["ManchesterUnited", "RedDevils"]
GENERAL_SUBREDDITS = ["soccer", "PremierLeague", "football"]


MU_NEWS_FEEDS = [
    "https://www.manutd.com/en/feeds/newsrssfeed",
    "https://www.manutd.com/Feeds/NewsSecondRSSFeed",   
]

GENERAL_NEWS_FEEDS = [
    "https://www.bbc.co.uk/sport/football/rss.xml",
    "https://www.espn.com/espn/rss/news",
    "https://www.theguardian.com/football/manchester-united/rss",
    "https://www.fourfourtwo.com/feeds.xml",
    "https://talksport.com/feed/",
]

# Main window
root = tk.Tk()
root.title("Manchester United Sentiment Analyzer")
root.geometry("800x900")

styles.apply_styles(root)

img = Image.open("assets/united_theme.png")
photo = ImageTk.PhotoImage(img)

# Main label
main_label = ttk.Label(root, text="Manchester United Sentiment Analyzer", font=("Arial", 16))
main_label.grid(row=0, column=0, columnspan=2, pady=15)

image_label = ttk.Label(root, image=photo)
image_label.image = photo 
image_label.grid(row=0, column=0, sticky="nw", padx=5, pady=5)

mu_frame = ttk.LabelFrame(root, text="Manchester United Fans", padding=(10,10))
mu_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

def analyze_mu():
    try:
        count = data_collection.fetch_reddit_json(MU_SUBREDDITS, True)
        
        # Step 2: run sentiment analysis on the CSV
        df = sentiment_analysis.analyze_csv_sentiment("data/reddit/mu_posts.csv")

        # Step 3: compute positive percentage
        pos_percent = (df["sentiment"]=="Positive").mean() * 100
        neg_percent = (df["sentiment"]=="Negative").mean() * 100
        neu_percent = (df["sentiment"]=="Neutral").mean() * 100

        # Step 4: display donut chart
        mu_red_donut.update(pos_percent, neg_percent, neu_percent)
        
    except Exception as e:
        messagebox.showerror(
        title="Error",
        message=f"Something went wrong:\n\n{e}"
    )

mu_button = ttk.Button(mu_frame, text="Analyze MU Fan Subreddit Sentiment", command=analyze_mu)
mu_button.grid(row=0, column=0, pady=5, sticky="ew")

mu_red_frame_chart = ttk.Frame(mu_frame)
mu_red_frame_chart.grid(row=1, column=0, pady=10)
mu_red_donut = donut_chart.DonutChart(mu_red_frame_chart)

gen_frame = ttk.LabelFrame(root, text="General Fans", padding=(10,10))
gen_frame.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

def analyze_general():
    try:
        count = data_collection.fetch_reddit_json(GENERAL_SUBREDDITS, False)
        
        # Step 2: run sentiment analysis on the CSV
        df = sentiment_analysis.analyze_csv_sentiment("data/reddit/general_posts.csv")

        # Step 3: compute positive percentage
        pos_percent = (df["sentiment"]=="Positive").mean() * 100
        neg_percent = (df["sentiment"]=="Negative").mean() * 100
        neu_percent = (df["sentiment"]=="Neutral").mean() * 100

        # Step 4: display donut chart
        gen_red_donut.update(pos_percent, neg_percent, neu_percent)
        
    except Exception as e:
        messagebox.showerror(
        title="Error",
        message=f"Something went wrong:\n\n{e}"
    )

gen_button = ttk.Button(gen_frame, text="Analyze General Football Subreddit Sentiment", command=analyze_general)
gen_button.grid(row=0, column=0, pady=5, sticky="ew")

gen_red_frame_chart = ttk.Frame(gen_frame)
gen_red_frame_chart.grid(row=1, column=0, pady=10)
gen_red_donut = donut_chart.DonutChart(gen_red_frame_chart)

def analyze_mu_news():
    try:
        # Step 1: fetch articles & save to CSV
        count, sources = data_collection.fetch_news_rss(MU_NEWS_FEEDS, mu_only=True)

        # Step 2: run sentiment analysis on the CSV
        df = sentiment_analysis.analyze_csv_sentiment("data/news/mu_articles.csv")

        # Step 3: compute positive percentage
        pos_percent = (df["sentiment"]=="Positive").mean() * 100
        neg_percent = (df["sentiment"]=="Negative").mean() * 100
        neu_percent = (df["sentiment"]=="Neutral").mean() * 100

        # Step 4: display donut chart
        mu_news_donut.update(pos_percent, neg_percent, neu_percent)

    except Exception as e:
        messagebox.showerror(
        title="Error",
        message=f"Something went wrong:\n\n{e}"
    )
       
mu_news_button = ttk.Button(mu_frame, text="Analyze MU Dedicated News Sentiment", command=analyze_mu_news)
mu_news_button.grid(row=2, column=0, pady=5, sticky="ew")

# Frame for the donut chart
mu_news_frame_chart = ttk.Frame(mu_frame)
mu_news_frame_chart.grid(row=3, column=0, pady=10)
mu_news_donut = donut_chart.DonutChart(mu_news_frame_chart)

def analyze_general_news_button():
    try:
        # Step 1: fetch articles & save to CSV
        count, sources = data_collection.fetch_news_rss(GENERAL_NEWS_FEEDS, mu_only=False)

        # Step 2: run sentiment analysis on the CSV
        df = sentiment_analysis.analyze_csv_sentiment("data/news/general_articles.csv")

        # Step 3: compute positive percentage
        pos_percent = (df["sentiment"]=="Positive").mean() * 100
        neg_percent = (df["sentiment"]=="Negative").mean() * 100
        neu_percent = (df["sentiment"]=="Neutral").mean() * 100

        # Step 4: display donut chart
        general_news_donut.update(pos_percent, neg_percent, neu_percent)

    except Exception as e:
        messagebox.showerror(
        title="Error",
        message=f"Something went wrong:\n\n{e}"
    )
        
general_news_button = ttk.Button(gen_frame, text="Analyze General News Sentiment", command=analyze_general_news_button)
general_news_button.grid(row=2, column=0, pady=5, sticky="ew")

# Frame for the donut chart
general_news_frame_chart = ttk.Frame(gen_frame)
general_news_frame_chart.grid(row=3, column=0, pady=10)
general_news_donut = donut_chart.DonutChart(general_news_frame_chart)

root.update_idletasks()

width = root.winfo_width()
height = root.winfo_height()

root.minsize(width, height)

# Configure grid weights to make sections resize nicely
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)

# Run the app
root.mainloop()
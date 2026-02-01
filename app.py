import tkinter as tk
from tkinter import ttk
from src import data_collection, donut_chart, sentiment_analysis, styles, validation
from tkinter import messagebox
from PIL import Image, ImageTk
 

root = tk.Tk()
root.title("Manchester United Sentiment Analyzer")
root.geometry("820x900")

styles.apply_styles(root)

analysis_info = {
    "mu_reddit": None,
    "general_reddit": None,
    "mu_news": None,
    "general_news": None
}

img = Image.open("assets/united_theme.png").resize((70, 70))
photo = ImageTk.PhotoImage(img)

main_label = ttk.Label(root, text="\nManchester United Sentiment Analyzer", font=("Arial", 16))
main_label.grid(row=0, column=0, columnspan=2, pady=10)

image_label = ttk.Label(root, image=photo, style="Image.TLabel")
image_label.grid(row=0, column=0, sticky="nw", padx=15, pady=5)

def show_about():
    messagebox.showinfo(
                "About",
        "This application performs sentiment analysis on Reddit and news headlines.\n\n"
        "It uses VADER, a rule-based sentiment analysis model, to classify each headline "
        "as Positive, Neutral, or Negative and presents the results as percentage summaries.\n\n"
        "The test tool allows you to upload a CSV file containing manually assigned sentiment "
        "labels. These are compared against VADER’s predictions using evaluation metrics "
        "such as accuracy and precision to assess performance in this context.\n\n"
        "Note: Sentiment analysis is inherently subjective, and results should be interpreted "
        "as indicative rather than definitive."
    )
    
def show_info(section):
    info = analysis_info.get(section)

    if not info:
        messagebox.showinfo(
            "Info",
            "No analysis has been run yet.\n\nPlease run the analysis first."
        )
        return

    lines = ["Sources used for this analysis:\n"]

    for source, count in info["sources"].items():
        lines.append(f"{source}: {count} titles")

    lines.append(f"\nTotal titles analysed: {info['total']}")

    text = "\n".join(lines)

    messagebox.showinfo("Source Information", text)

about_btn = styles.create_info_dot(root, command=show_about)
about_btn.grid(row=0, column=1, sticky="ne", padx=5, pady=5)

test_btn = styles.create_test_dot(root, command=lambda: validation.open_test_window(root))
test_btn.grid(row=0, column=1, sticky="ne", padx=(0, 30), pady=5)

mu_frame = ttk.LabelFrame(root, padding=(10, 10))
mu_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

def analyze_mu():
    try:
        total_count, source_count = data_collection.fetch_reddit_json("mu", True)
        
        df = sentiment_analysis.analyze_csv_sentiment("data/reddit/mu_posts.csv")

        pos_percent = (df["sentiment"]=="Positive").mean() * 100
        neg_percent = (df["sentiment"]=="Negative").mean() * 100
        neu_percent = (df["sentiment"]=="Neutral").mean() * 100

        mu_red_donut.update(pos_percent, neg_percent, neu_percent)
        
        analysis_info["mu_reddit"] = {
            "total": total_count,
            "sources": source_count
        }
        
    except Exception as e:
        messagebox.showerror(
        title="Error",
        message=f"Something went wrong:\n\n{e}"
    )

mu_button = ttk.Button(mu_frame, text="Analyze MU Fan Subreddit Sentiment", style="Action.TButton", command=analyze_mu)
mu_button.grid(row=0, column=0, pady=5, sticky="ew")

mu_red_frame_chart = ttk.Frame(mu_frame)
mu_red_frame_chart.grid(row=1, column=0, pady=10)
mu_red_donut = donut_chart.DonutChart(mu_red_frame_chart)

mu_info_btn = styles.create_info_dot(mu_frame, command=lambda: show_info("mu_reddit"))
mu_info_btn.grid(row=1, column=0, sticky="ne", padx=1, pady=1)

gen_frame = ttk.LabelFrame(root, padding=(10,10))
gen_frame.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

def analyze_general():
    try:
        total_count, source_count = data_collection.fetch_reddit_json("gen", False)
        
        # Step 2: run sentiment analysis on the CSV
        df = sentiment_analysis.analyze_csv_sentiment("data/reddit/general_posts.csv")

        # Step 3: compute positive percentage
        pos_percent = (df["sentiment"]=="Positive").mean() * 100
        neg_percent = (df["sentiment"]=="Negative").mean() * 100
        neu_percent = (df["sentiment"]=="Neutral").mean() * 100

        # Step 4: display donut chart
        gen_red_donut.update(pos_percent, neg_percent, neu_percent)
        
        analysis_info["general_reddit"] = {
            "total": total_count,
            "sources": source_count
        }
        
    except Exception as e:
        messagebox.showerror(
        title="Error",
        message=f"Something went wrong:\n\n{e}"
    )

gen_button = ttk.Button(gen_frame, text="Analyze General Football Subreddit Sentiment", style="Action.TButton", command=analyze_general)
gen_button.grid(row=0, column=0, pady=5, sticky="ew")

gen_red_frame_chart = ttk.Frame(gen_frame)
gen_red_frame_chart.grid(row=1, column=0, pady=10)
gen_red_donut = donut_chart.DonutChart(gen_red_frame_chart)

gen_info_btn = styles.create_info_dot(gen_frame,  command=lambda: show_info("general_reddit"))
gen_info_btn.grid(row=1, column=0, sticky="ne", padx=1, pady=1)

def analyze_mu_news():
    try:
        # Step 1: fetch articles & save to CSV
        total_count, source_count = data_collection.fetch_news_rss("mu", mu_only=True)

        # Step 2: run sentiment analysis on the CSV
        df = sentiment_analysis.analyze_csv_sentiment("data/news/mu_articles.csv")

        # Step 3: compute positive percentage
        pos_percent = (df["sentiment"]=="Positive").mean() * 100
        neg_percent = (df["sentiment"]=="Negative").mean() * 100
        neu_percent = (df["sentiment"]=="Neutral").mean() * 100

        # Step 4: display donut chart
        mu_news_donut.update(pos_percent, neg_percent, neu_percent)
        
        analysis_info["mu_news"] = {
            "total": total_count,
            "sources": source_count
        }

    except Exception as e:
        messagebox.showerror(
        title="Error",
        message=f"Something went wrong:\n\n{e}"
    )
       
mu_news_button = ttk.Button(mu_frame, text="Analyze MU Dedicated News Sentiment", style="Action.TButton", command=analyze_mu_news)
mu_news_button.grid(row=2, column=0, pady=5, sticky="ew")

mu_news_frame_chart = ttk.Frame(mu_frame)
mu_news_frame_chart.grid(row=3, column=0, pady=10)
mu_news_donut = donut_chart.DonutChart(mu_news_frame_chart)

mu_news_info_btn = styles.create_info_dot(mu_frame, command=lambda: show_info("mu_news"))
mu_news_info_btn.grid(row=3, column=0, sticky="ne", padx=1, pady=1)

def analyze_general_news_button():
    try:
        # Step 1: fetch articles & save to CSV
        total_count, source_count = data_collection.fetch_news_rss("gen", mu_only=False)

        # Step 2: run sentiment analysis on the CSV
        df = sentiment_analysis.analyze_csv_sentiment("data/news/general_articles.csv")

        # Step 3: compute positive percentage
        pos_percent = (df["sentiment"]=="Positive").mean() * 100
        neg_percent = (df["sentiment"]=="Negative").mean() * 100
        neu_percent = (df["sentiment"]=="Neutral").mean() * 100

        # Step 4: display donut chart
        general_news_donut.update(pos_percent, neg_percent, neu_percent)
        
        analysis_info["general_news"] = {
            "total": total_count,
            "sources": source_count
        }

    except Exception as e:
        messagebox.showerror(
        title="Error",
        message=f"Something went wrong:\n\n{e}"
    )
        
general_news_button = ttk.Button(gen_frame, text="Analyze General News Sentiment", style="Action.TButton", command=analyze_general_news_button)
general_news_button.grid(row=2, column=0, pady=5, sticky="ew")

general_news_frame_chart = ttk.Frame(gen_frame)
general_news_frame_chart.grid(row=3, column=0, pady=10)
general_news_donut = donut_chart.DonutChart(general_news_frame_chart)

gen_news_info_btn = styles.create_info_dot(gen_frame, command=lambda: show_info("general_news"))
gen_news_info_btn.grid(row=3, column=0, sticky="ne", padx=1, pady=1)

root.update_idletasks()

width = root.winfo_width()
height = root.winfo_height()

root.minsize(width, height)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)

# Run the app
root.mainloop()



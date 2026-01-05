import tkinter as tk
from tkinter import ttk
from src import data_collection

# Subreddit groups
MU_SUBREDDITS = ["ManchesterUnited", "RedDevils"]
GENERAL_SUBREDDITS = ["soccer", "PremierLeague", "football"]

# Main window
root = tk.Tk()
root.title("Manchester United Sentiment Analyzer")
root.geometry("600x500")  # width x height

# Main label
main_label = ttk.Label(root, text="Manchester United Sentiment Analyzer", font=("Arial", 16))
main_label.grid(row=0, column=0, columnspan=2, pady=15)

# -------------------------------
# Manchester United Fans Section
# -------------------------------
mu_frame = ttk.LabelFrame(root, text="Manchester United Fans", padding=(10,10))
mu_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

def analyze_mu():
    try:
        count = data_collection.fetch_reddit_json(MU_SUBREDDITS)
        mu_output.config(
            text=f"Fetched {count} posts from MU fan subreddits.\nSaved to data/reddit/posts_mu.csv"
        )
    except Exception as e:
        mu_output.config(text=f"Error:\n{e}")

mu_button = ttk.Button(mu_frame, text="Analyze MU Fan Subreddit Sentiment", command=analyze_mu)
mu_button.grid(row=0, column=0, pady=5, sticky="ew")

mu_output = ttk.Label(mu_frame, text="Results will appear here.", font=("Arial", 12))
mu_output.grid(row=1, column=0, pady=5, sticky="w")

# -------------------------------
# General Fans Section
# -------------------------------
gen_frame = ttk.LabelFrame(root, text="General Fans", padding=(10,10))
gen_frame.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

def analyze_general():
    try:
        count = data_collection.fetch_reddit_json(GENERAL_SUBREDDITS)
        gen_output.config(
            text=f"Fetched {count} posts from general football subreddits.\nSaved to data/reddit/posts_general.csv"
        )
    except Exception as e:
        gen_output.config(text=f"Error:\n{e}")

gen_button = ttk.Button(gen_frame, text="Analyze General Football Subreddit Sentiment", command=analyze_general)
gen_button.grid(row=0, column=0, pady=5, sticky="ew")

gen_output = ttk.Label(gen_frame, text="Results will appear here.", font=("Arial", 12))
gen_output.grid(row=1, column=0, pady=5, sticky="w")

# Configure grid weights to make sections resize nicely
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)

# Run the app
root.mainloop()
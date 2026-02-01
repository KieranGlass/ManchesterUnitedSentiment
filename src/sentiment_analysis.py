import tkinter as tk
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

nltk.download("vader_lexicon")

sia = SentimentIntensityAnalyzer()

def label_sentiment(compound):
    """Label compound score as Positive, Neutral, or Negative"""
    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    else:
        return "Neutral"
    
"""
    
def compute_weight(row):
    weight = 1.0

    if row.get("level") == "title":
        weight *= 1.5

    depth = row.get("depth", 0)
    if depth > 1:
        weight *= 0.5

    score = row.get("score", 0)
    if score > 50:
        weight *= 1.3
    elif score < 0:
        weight *= 0.7

    return weight
    
"""

def analyze_csv_sentiment(csv_path):
    
    df = pd.read_csv(csv_path)
    
    df["compound"] = df["text"].apply(lambda x: sia.polarity_scores(x)["compound"])
    df["neg"] = df["text"].apply(lambda x: sia.polarity_scores(x)["neg"])
    df["neu"] = df["text"].apply(lambda x: sia.polarity_scores(x)["neu"])
    df["pos"] = df["text"].apply(lambda x: sia.polarity_scores(x)["pos"])
    
    df["sentiment"] = df["compound"].apply(label_sentiment)
    
    # if apply_weighting:
        # df["weight"] = df.apply(compute_weight, axis=1)
        # df["weighted_compound"] = df["compound"] * df["weight"]

    return df
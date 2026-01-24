import tkinter as tk
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt


# nltk.download("vader_lexicon")

sia = SentimentIntensityAnalyzer()

def label_sentiment(compound):
    """Label compound score as Positive, Neutral, or Negative"""
    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def analyze_csv_sentiment(csv_path):
    """
    Reads a CSV with at least a 'text' column, adds VADER sentiment scores
    and returns the DataFrame.
    """
    df = pd.read_csv(csv_path)
    
    df["compound"] = df["text"].apply(lambda x: sia.polarity_scores(x)["compound"])
    df["neg"] = df["text"].apply(lambda x: sia.polarity_scores(x)["neg"])
    df["neu"] = df["text"].apply(lambda x: sia.polarity_scores(x)["neu"])
    df["pos"] = df["text"].apply(lambda x: sia.polarity_scores(x)["pos"])
    
    df["sentiment"] = df["compound"].apply(label_sentiment)
    
    return df
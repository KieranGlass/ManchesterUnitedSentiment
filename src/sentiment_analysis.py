import tkinter as tk
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

nltk.download("vader_lexicon")

"""
Sentiment Analysis Module

Implements rule-based sentiment classification using NLTK's VADER
SentimentIntensityAnalyzer() 

This module:

- Applies VADER polarity scoring to text datasets  
- Extracts compound, positive, neutral, and negative sentiment values  
- Converts compound scores into readable sentiment labels 

Compound is from -1 to 1 and the neutral band is set at -0.05 - 0.05,
which is quite small and easily changed

label_sentiment method handles the labelling and modifying this method
can add extra layers of sentiment for a more in depth look at how 
stong sentiment is. Current app may show 70% positive and 30% negative, 
however there may be no positive sentiment above 0.5 in those results and 
majority of the negative sentiment could be -0.9  

The resulting sentiment data is passed on to the visualisation module

Note: commented out compute_weight method is part of fucntioanlity that
looked to take sentiment from reddit comments and apply a weighting to 
liked comments as oppose to downvoted comments. Reddit API limits prevented
it from being integrated for now

"""

sia = SentimentIntensityAnalyzer()

def label_sentiment(compound):

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
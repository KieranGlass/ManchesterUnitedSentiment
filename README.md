# Sentiment Analysis Application - IU AI Project

An application that uses the **VADER sentiment analysis tool** designed to detect whether a piece of text expresses a positive, negative, or neutral sentiment.

## App Details:

Program provides a snapshot of the current sentiment amongst fans and journalists in the context of Manchester United football club.

Through use of the app's GUI, a user can assess current sentiment from Manchester United related reddit threads and general football related reddit threads,
they can also assess the sentiment of news articles from Manchester United dedicated media and separately general media.

Sentiment of people involved with the football club and the wider footballing world is separated as people involved with the club tend to be more passionate
and therefore more likely to have expressions of extreme sentiment.

NOTE: App is configured to work for Manchester United solely through the use of Keyword and Thread Constant variables. Altering these constant values in the code base 
to any other club can quickly change the focus of the application without needing change in logic

App includes a Test tool for examining the validity of the app and VADER within its context. User can upload a CSV file (Must have at least a 'text' field and
'manual_sentiment' field) and run VADER analysis on it (doesn't have to be about Manchester United). 

Evaluation Metrics and a confusion matrix are returned to provide an overview of the applications effectiveness.

## Installation.

It is recommended to install the project dependencies inside a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # macOS / Linux
.\venv\Scripts\activate       # Windows
```

then to prepare the environment for the application

```pip install -r requirements.txt```


## Using the App.

In order to start the GUI, when located in folder run

```python app.py```

GUI will appear and the data collection process begins by clicking one of the labelled buttons. Testing tool can be accessed next to the about button in the top
right of the window.

## Python Version and Environment

Project designed to work with Python 3.10 or later, earlier versions may cause runtime errors or unexpected behaviour
It is recommended to run the application inside a **virtual environment**.

## SSL certificates

App runs nltk.download() statements which may cause app to fail due to missing SSL certificates, more common on macOS. 
See: https://docs.python.org/3/using/mac.html#installing-on-macos






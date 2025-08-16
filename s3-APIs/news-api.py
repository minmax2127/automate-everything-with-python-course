"""
News API Integration
---------------------
Connects the Python app to the newsapi.org API and gets news data from it based on timeframe and topic assigned
Example URL: "https://newsapi.org/v2/everything?q=bitcoin&?from=2025-08-16T05:35:34&to=2025-08-01T05:35:34&apiKey=17d5274405dc4cb2b68cbf3d5a30aac4"
"""

import requests
import json
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()
NEWS_API_KEY = os.environ.get("news_api_key")

def get_news(topic, from_date, to_date, api_key = NEWS_API_KEY):
    """ Calls API and returns news based on the arguments passed """
    url = f"https://newsapi.org/v2/everything?q={topic}&?from={from_date}&to={to_date}&apiKey={api_key}"
    print(url)
    data = requests.get(url).json()
    return data["articles"]

def format_date(date_str):
    """ Formats date into the acceptable format for the api """
    dt = datetime.strptime(date_str, "%Y/%m/%d")
    dt_string = f"{dt.strftime("%Y")}-{dt.strftime("%m")}-{dt.strftime("%d")}"
    return dt_string
    

if __name__ == "__main__":
    # get user input
    topic = input("Enter topic: ")
    from_date = format_date(input("Enter from date (yyyy/mm/dd): "))
    to_date = format_date(input("Enter to date (yyyy/mm/dd): "))
    
    # get search results
    search_results = get_news(topic, from_date, to_date)
    
    # display results
    for i, article in enumerate(search_results):
        print(f"#{i + 1}: {article["title"]}")
"""
Stock Data Downloader
---------------------
Downloads any company stock data from Yahoo Finance 
"""
# import libraries
import requests
from datetime import datetime
import time

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
}

# ask for user input
ticker_code = input("Enter company ticker code: ")
from_date = input("Enter start date in yyyy/mm/dd format: ")
to_date = input("Enter end date in yyyy/mm/dd format: ")

from_datetime = datetime.strptime(from_date, "%Y/%m/%d")
to_datetime = datetime.strptime(to_date, "%Y/%m/%d")

from_epoch = int(time.mktime(from_datetime.timetuple()))
to_epoch = int(time.mktime(to_datetime.timetuple()))

url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker_code}?period={from_epoch}period2={to_epoch}&interval=1d&events=history&includeAdjustedClose=true"

print(url)
# make request
# content = requests.get(url, headers = headers).content
# print(content)
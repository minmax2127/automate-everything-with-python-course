"""
Currency Rate Web Scraper
--------------------------
Scrapes a currency converter website using Beautiful Soup
Example URL: www.x-rates.com/calculator/?from=EUR&to=USD&amount=1
"""
import requests
from bs4 import BeautifulSoup


def get_rate(from_currency, to_currency, amount = "1.0"):
    """ Scrapes the website and returns the rate """
    # store the html data in a soup
    URL = f"https://www.x-rates.com/calculator/?from={from_currency}&to={to_currency}&amount={amount}"
    content = requests.get(URL).text
    soup = BeautifulSoup(content, "html.parser")

    # get the rate and clean the text
    rate = soup.find("span", class_="ccOutputRslt").text
    rate = float(rate.split(" ")[0])
    return rate


if __name__ == "__main__":
    # get input
    from_currency = input("Enter current currency: ")
    to_currency = input("Enter currency to convert to : ")
    amount = str(float(input("Amount: ")))

    # scrape the website for the rate
    rate = get_rate(from_currency, to_currency, amount)
    print(rate)
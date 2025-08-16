"""
Countries of the World - Webscraper
-----------------------------------
Scrapes a mock website with a list of the countries in the world. Use this for practice of BeautifulSoup
"""
from bs4 import BeautifulSoup
import requests

URL = "https://www.scrapethissite.com/pages/simple/"

def get_country_list(url):
    """ Returns a list of countries scraped from the website """
    content = requests.get(url).text
    soup = BeautifulSoup(content, "html.parser")
    country_elements = list(soup.find_all("h3", class_="country-name"))
    countries = [(lambda x: x.text.strip())(country) for country in country_elements]
    return countries

if __name__ == '__main__':
    countries = get_country_list(URL)
    print(countries)
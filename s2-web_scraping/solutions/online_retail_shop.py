"""
Web Scraper with Automated Login
--------------------------------
Logs into a webste and scrapes static and dynamic text from the homepage.
Creates a txt file every 2 seconds that stores the newly scraped dynamic text.

Output filename: <year>-<month>-<day>.<hour>-<mins>-<seconds>.txt
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import time
from datetime import datetime
from dotenv import load_dotenv


# Configuration
CHROME_DRIVER_PATH = "C:\\Users\\Maxine\\Documents\\courses\\automate-everything-with-python-course\\s2-web_scraping\\chromedriver.exe"
TITAN_22_URL = "https://titan22.com/account/login?return_url=%2Faccount"

load_dotenv()

# Demo Credentials (stored in environment variables or fallback for demo)
CREDENTIALS = {
    "email": os.environ.get("secretEmail"), 
    "password": os.environ.get("secretPassword")
}   

CHROME_ARGUMENTS = [
    "disable-infobars", 
    "start-maximized", 
    "disable-dev-shm-usage", 
    "no-sandbox", 
    "disable-blink-features=AutomationControlled"
]

def get_driver(url):
    """ Returns the driver with custom options and navigate to the web url """
    options = webdriver.ChromeOptions()
    # add arguments to the options

    for arg in CHROME_ARGUMENTS:
        options.add_argument(arg)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # create driver and configure its settings
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    return driver

def wait_for_element(driver, by, value, timeout = 10):
    """ Wait for the element to be present on the page then return it """
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

if __name__ == "__main__":
    driver = get_driver(TITAN_22_URL)
    driver.find_element(by = By.ID, value = "CustomerEmail").send_keys(CREDENTIALS["email"])
    time.sleep(2)
    driver.find_element(by = By.ID, value = "CustomerPassword").send_keys(CREDENTIALS["password"] + Keys.RETURN)
    time.sleep(2)
    driver.find_element(by = By.XPATH, value = '//*[@id="shopify-section-footer"]/section/div/div[1]/div[1]/div[1]/nav/ul/li[1]/a').click()
    print(driver.current_url)
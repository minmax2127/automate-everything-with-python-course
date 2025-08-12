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

# Configuration
CHROME_DRIVER_PATH = "C:\\Users\\Maxine\\Documents\\courses\\automate-everything-with-python-course\\s2-web_scraping\\chromedriver.exe"
WEB_URL = "http://automated.pythonanywhere.com/login/"

# Demo Credentials (stored in environment variables or fallback for demo)
USERNAME = os.getenv("WEB_SCRAPER_USER", "automated")
PASSWORD = os.getenv("WEB_SCRAPER_PASSWORD", "automatedautomated")

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

def get_element_text(driver, by, value):
    """ Returns the extracted text from a website tag """
    element = wait_for_element(driver, by, value)
    return element.text

def scrape_homepage(driver):
    """ Scrapes the Homepage for the static and dynamic value"""
    time.sleep(2)

    static_text = get_element_text(driver, By.XPATH, "/html/body/div[1]/div/h1[1]")
    dynamic_text = get_element_text(driver, By.XPATH, "/html/body/div[1]/div/h1[2]")

    # filter dynamic text
    dynamic_text = dynamic_text.split(': ', 1)[1]


    return static_text, dynamic_text

def create_new_outfile(data):
    # create new file name
    now = datetime.now()
    outfile = now.strftime("%Y-%m-%d.%H-%M-%S") + ".txt"

    # create new file and store the data
    f = open(outfile, "w")
    f.write(data)

    # close the file
    f.close()

if __name__ == "__main__":
    try:
        driver = get_driver(WEB_URL)
    except RuntimeError:
        print('URL Unaccessed')
        exit()
    

    # Login
    username_input = wait_for_element(driver, By.ID, "id_username").send_keys(USERNAME)
    password_input = wait_for_element(driver, By.ID, "id_password").send_keys(PASSWORD + Keys.RETURN)
    
    # Navigate to homepage
    home_button = wait_for_element(driver, By.XPATH,  "/html/body/nav/div/a").click()
    
    # Extract dynamic data every 2 seconds
    for _ in range(10):
        static, dynamic = scrape_homepage(driver)
        create_new_outfile(dynamic)

    print("\n10 Files saved!")
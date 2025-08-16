"""
Log In Automator
----------------
Proper way of logging in to a website with required user authentication in Github
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service

from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_LOGIN_PAGE = "https://github.com/login"
GITHUB_CREDENTIALS = {
    "username": os.environ.get("secretUsername"), 
    "password": os.environ.get("secretPassword")
}
CHROME_DRIVER_PATH = "C:\\Users\\Maxine\\Documents\\courses\\automate-everything-with-python-course\\s2-web_scraping\\chromedriver.exe"


# initialize the Chrome driver
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)

### PART 1: Logging In  ###

# head to github login page
driver.get(GITHUB_LOGIN_PAGE)
driver.find_element("id", "login_field").send_keys(GITHUB_CREDENTIALS["username"])
driver.find_element("id", "password").send_keys(GITHUB_CREDENTIALS["password"])

# click login button
driver.find_element("name", "commit").click()


WebDriverWait(driver = driver, timeout = 10).until(
    lambda x: x.execute_script("return document.readyState === 'complete'")
)

error_message = "Incorrect username or password"

# get the errors (if there are)
errors = driver.find_elements("css selector", ".flash-error")

if any(error_message in e.text for e in errors):
    print("[!] Login failed")
else:
    print("[+] Login Successful")


### PART 2 EXTRACT PUBLIC REPOSITORIES  ###
repos = driver.find_element("css selector", ".js-repos-container")

# wait for the repos container to be loaded
WebDriverWait(driver = driver, timeout = 10).until((
    lambda x: repos.text != "Loading..."
))

# iterate over the repos and print their names
for repo in repos.find_elements("css selector", "li.public"):
    print(repo.find_element("css selector", "a").get_attribute("href"))

# close the driver
driver.close()
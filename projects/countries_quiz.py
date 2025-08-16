"""
Quiz on Countries
-----------------
Uses the scraped country data to create a simple quiz on countries

DEMO
----
Enter Player Name: Maxine

WELCOME MAXINE!

Lives: ❤️❤️❤️
Question #1: Country that capital of "Victoria"
a. Sudan
b. Philippines
c. Seychelles

Answer: a

You're wrong!
Lives: ❤️❤️
Question #1: Country that capital of "Bangkok"
a. Turkey
b. Taiwan
c. Vatican City

Answer: b

You're correct!

- Player starts with 0 points
- For each correct answer, player gets 50 points
"""

import os
import time
from bs4 import BeautifulSoup
import requests
import json
import random

countries_json = {
    "countries": [
        {
            "name": "Andorra", 
            "capital": "Andorra la Vella", 
            "population": 84000, 
            "area": 468.0
        }, 
        {
            "name": "United Arab Emirates", 
            "capital": "Abu Dhabi", 
            "population": 4975593, 
            "area": 82880.0
        }, 
        {
            "name": "Afghanistan", 
            "capital": "Kabul", 
            "population": 29121286, 
            "area": 647500.0
        },
        {
            "name": "Antigua and Barbuda", 
            "capital": "St. John's", 
            "population": 86754, 
            "area": 443.0
        },
        {
            "name": "Anguilla", 
            "capital": "The Valley", 
            "population": 13254, 
            "area": 102.0
        },
        {
            "name": "Albania", 
            "capital": "Tirana", 
            "population": 2986952, 
            "area": 28748.0
        }
    ]
}

COUNTRIES_URL = "https://www.scrapethissite.com/pages/simple/"

def clear_screen(delay = 0.2):
    """ Clears the terminal screen after a delay """
    time.sleep(delay)
    os.system('cls')

def press_enter():
    """ Requires player to press enter """
    enter = input("\n\nPRESS [ENTER] to proceed...")


def ask_question(question, choices = []):
    """ Asks a given question to the player and ensures that their answer is within the choices """
    choices = [(lambda x: x.lower())(choice) for choice in choices]
    while True:
        answer = input(question)
        clear_screen()
        # if no choices given, any user input is acceptable
        if len(choices) == 0:
            return answer
        else:
            # if answer is in the choices, accept user input. else, repeat question
            if answer.lower() in choices:
                return answer
            else:
                print("Invalid answer!\n")

class Data:
    """ Handles the backend of the game, which is all about the retrieval of data from the url to webscrape"""
    def __init__(self, url):
        self.url = url
        self.countries = self.get_countries_data(self.url)

    def get_countries_data(self, url):
        """ Returns the list of countries along with their details """
        content = requests.get(url).text
        soup = BeautifulSoup(content, "html.parser")
        countries = list(soup.find_all("div", class_="col-md-4 country"))

        # store the country details in a list
        country_list = []
        for country in countries:
            country = str(country)
            country_soup = BeautifulSoup(country, "html.parser")

            name_tag = country_soup.find("h3", class_="country-name")
            capital_tag = country_soup.find("span", class_="country-capital")
            population_tag = country_soup.find("span", class_="country-population")
            area_tag = country_soup.find("span", class_="country-area")

            data = {
                "name": name_tag.text.strip(), 
                "capital": capital_tag.text.strip(), 
                "population": population_tag.text.strip(), 
                "area": area_tag.text.strip(), 
            }
            country_list.append(data)

        return country_list
    
    def formulate_question(self, country):
        """ Returns formulated question, answer, and choices """
        question = f"Which country has a capital of {country["capital"]}?"
        answer = f"{country["name"]}"

        # generate choices
        choices = [answer]
        country_names = [(lambda x: x["name"])(country) for country in self.countries]
        country_names.remove(answer)
        random.shuffle(country_names)
        choices = country_names[:2]
        choices.append(answer)
        random.shuffle(choices)

        choices = {
            "a": choices[0], 
            "b": choices[1], 
            "c": choices[2]
        }
            
        return question, answer, choices
    
    def validate_answer(self, player_answer, answer, choices):
        """ Checks if the player answereed correctly or not """
        print("player_answer: ", player_answer)
        print("answer: ", answer)
        print("choices: ", choices)

        return True

if __name__ == '__main__':
    """
    name = ask_question("Enter name: ")
    screen = Screens(name, lives = 3)
    screen.Welcome_Screen()
    """
    # game data
    round_no = 0
    lives_left = 3

    # fetch data
    data = Data(COUNTRIES_URL)

    # game loop
    while lives_left != 0:
        # round question and answer
        country = random.choice(data.countries)
        question, answer, choices = data.formulate_question(country)

        # ask player the question
        player_answer = ask_question(question + ": ", ["a", "b", "c"])
        is_correct = data.validate_answer(player_answer, answer, choices)


        break
































'''

class Screens:
    """ A class of the screens that would be displayed """
    def __init__(self, name, lives = 0):
        self.name = name
        self.lives = lives

    def Welcome_Screen(self):
        # display welcome message and instructions
        print(f"Welcome, {name}!")
        print("\nWe are happy to have you. Here are the mechanics of the game:")
        print("\nYou will be given 3 lives, and you must make the most out of it. \nIn this game, you need to go through a series of questions, wherein you need to match the country with its capital. \nDon't worry, there will be choices of course!")
        print("\n\nGOODLUCK, BABE!")
        press_enter()

    def Round_Screen(self, round_no):
        # display for each round
        # must have: Lives, Round no, Question, choices, input answer
        pass

        '''

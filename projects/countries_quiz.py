"""
Quiz on Countries
-----------------
Uses the scraped country data to create a simple quiz on countries

Features:
- Gameplay
- Saves data for offline game database
"""

import os
import time
from bs4 import BeautifulSoup
import requests
import random
import json

COUNTRIES_URL = "https://www.scrapethissite.com/pages/simple/"
SAVED_COUNTRY_DATA_FILEPATH = "countries.csv"

class Frontend:
    """ Handles the display-related factors of the game"""

    def clear_screen(self, delay = 0.2):
        """ Clears the terminal screen after a delay """
        time.sleep(delay)
        os.system('cls')

    def press_enter(self, ):
        """ Requires player to press enter """
        enter = input("\n\nPRESS [ENTER] to proceed...")

    def ask_question(self, question, choices = []):
        """ Asks a given question to the player and ensures that their answer is within the choices """
        choices = [(lambda x: x.lower())(choice) for choice in choices]
        while True:
            answer = input(question)
            print()
            # if no choices given, any user input is acceptable
            if len(choices) == 0:
                return answer
            else:
                # if answer is in the choices, accept user input. else, repeat question
                if answer.lower() in choices:
                    return answer
                else:
                    print("Invalid answer!\n")

    def display_choices(self, choices):
        """ Show the choices """
        for key, value in choices.items():
            print(f"{key}. {value}")

class Backend:
    """ Handles the backend of the game, which is all about the retrieval of data from the url to webscrape """
    def __init__(self, url):
        self.url = url
        self.countries = self.get_countries_data(self.url)

    def get_countries_data(self, url):
        """ Returns the list of countries along with their details """
        # check if country data has been saved before
        if os.path.exists(SAVED_COUNTRY_DATA_FILEPATH):
            return self.load_saved_country_data(SAVED_COUNTRY_DATA_FILEPATH)
        else:
            return self.scrape_country_data(url)
    
    def load_saved_country_data(self, filepath):
        """ Returns the json data of the country data stored in the csv """
        # store in a list
        country_list = []

        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                # create list of the data
                country_data = f.readline().split(",")[:4]

                # clean data
                country_data = [(lambda x: x.strip())(el) for el in country_data]
                if len(country_data) != 4:
                    continue
                
                # create json and append it to the list
                country_json = {
                    "name": str(country_data[0]), 
                    "capital": str(country_data[1]), 
                    "population": str(country_data[2]), 
                    "area": str(country_data[3]), 
                }
                country_list.append(country_json)

        return country_list


    def scrape_country_data(self, url):
        """ Scrapes the website for the data of the countries """
        try:
            # makes a request to the url
            r = requests.get(url, timeout=3)
            r.raise_for_status()
            content = r.text
        except Exception as e:
            # returns error message when HTTPError occurs. Exits program.  
            print(f"Error occurred!: {e}")
            exit()

        # creates soup for the html extracted
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

        self.save_country_data(country_list)

        return country_list
    
    def append_csv_row(self, f, lst):
        """ Creates a new row given a list and appends it to a csv file """
        for item in lst:
            item = str(item)
            if item:
                f.write(item)
            else:
                f.write("None")
            f.write(", ")
        f.write("\n")

    def save_country_data(self, country_list, filepath = SAVED_COUNTRY_DATA_FILEPATH):
        """ Saves scraped country data to a csv file """
        # create a file
        f = open(SAVED_COUNTRY_DATA_FILEPATH, "w", encoding="utf-8")

        # write header
        headers = ["Name", "Capital", "Population", "Area"]
        self.append_csv_row(f, headers)

        # create row for each country
        for i, country in enumerate(country_list):
            try:
                country_data = [country["name"], country["capital"], country["population"], country["area"]]
                self.append_csv_row(f, country_data)
            except Exception as e:
                print("Error at: ", e, i, country_list[i])
        
        # close file
        f.close()

    
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
        print(f"Player: {player_answer}, Answer: {answer}")
        is_correct = choices[player_answer] == answer
        
        if is_correct:
            print("Correct!")
        else:
            print(f"Wrong! Correct answer is {answer}.")

        return is_correct



if __name__ == '__main__':
    # create instances of the classes
    frontend = Frontend()
    backend = Backend(COUNTRIES_URL)

    # game data
    round_no = 1
    lives_left = 3
    points = 0

    # game loop
    while lives_left != 0:
        # get question and answer
        country = random.choice(backend.countries)
        question, answer, choices = backend.formulate_question(country)

        # display lives
        print(f"\nROUND # {round_no}")
        print("\nLives: ", "❤️" * lives_left)
        print(f"Points: {points}")

        # ask player the question
        print(f"\n{question}")
        frontend.display_choices(choices)
        player_answer = frontend.ask_question("Your answer: ", ["a", "b", "c"]).lower()
        
        # check if the answer is correct
        is_correct = backend.validate_answer(player_answer, answer, choices)
        
        # lose a life if answer is incorrect
        if not is_correct:
            lives_left -= 1
        else:
            points += 50

        # increment another round
        if lives_left != 0:
            round_no += 1

        frontend.clear_screen(1)

    # game over
    print(f"GAME OVER! You got {points}.")
    
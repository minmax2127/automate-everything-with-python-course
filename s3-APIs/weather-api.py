"""
Weather Data Logger
-------------------
Creates a csv file of the weather data from the OpenWeatherMap.org API
Forecast URL: https://api.openweathermap.org/data/2.5/forecast?q=Naga&APPID=<apikey>&units=metric
"""
import os
import requests

from dotenv import load_dotenv

load_dotenv()

WEATHER_KEY = os.environ.get("open_weather_map_api_key")
OUTFILE = "city_weather.csv"

def get_weather_data(city_name, apikey = WEATHER_KEY):
    """ Calls weather api and returns weather data based on Latitude and Longitude """
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&APPID={apikey}&units=metric"
    data = requests.get(url).json()
    return data["list"]
    

if __name__ == "__main__":
    # open filestream
    f = open(OUTFILE, "a")

    # get user input for city
    city = input("Enter city name: ").strip()

    # get weather data from API
    weather_data = get_weather_data(city)
    for data in weather_data:
        city_name = city
        time_str = data["dt_txt"]
        temperature = data["main"]["temp"]
        condition = data["weather"][0]["description"]
        f.write(f"{city_name}, {time_str}, {temperature}, {condition}\n")

    # close filestream
    f.close()

    print(f"Saved data in {OUTFILE}")

        
        



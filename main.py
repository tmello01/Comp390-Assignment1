import requests
import datetime
import url_factory
import configparser
from errors import LocationError, CurrentForecastError, QuotaReachedError
from url_factory import create_location_url

config = configparser.ConfigParser()

try:
    config.read("app.config")
    key = config["secrets"]["Key"]
except KeyError as ke:
    print(f"I'm sorry! We could not find the API Key. Please set the [secrets] 'Key' section in the app.config and try again!")
    exit(1)
except Exception as e: #handle any other exception we're not sure of. 
    print("I'm sorry! Something went wrong trying to read the config file. Please try again!")
    print(e)
    raise


def main():
    try:
        location = ask_for_location()
        if location is None:
            print("I'm sorry, we couldn't find your location. Please try living elsewhere.")
            exit(0)
        print("----------------------------------------")
        get_current_weather(location)
        print("----------------------------------------")
        get_forecast(location)
    except Exception as e:
        print(str(e))


def get_current_weather(location_code):
    try:
        current_weather = requests.get(url_factory.create_current_url(key, location_code)).json()
        print(f'The weather today is {current_weather[0]["WeatherText"]}!')
        print(f'The current temperature is {current_weather[0]["Temperature"]["Imperial"]["Value"]}° F')
        print(f'There is {"no rain right now. Enjoy it while it lasts!" if not current_weather[0]["HasPrecipitation"] else "rain right now. Grab a raincoat! 🧥"}')
    except Exception as e:
        raise CurrentForecastError(f"There was a problem getting the current weather. Please try again later!")


def get_forecast(location_code):
    five_day_forecast = requests.get(url_factory.create_five_day_url(key, location_code)).json()["DailyForecasts"]
    print("Five Day Forecast!: ")
    print('--------------------------------------------------------')
    for dayNum in range(0, 5):
        date = datetime.datetime.fromtimestamp(five_day_forecast[dayNum]["EpochDate"]).strftime("%a %m/%d")
        print(f'|{date}   |    {five_day_forecast[dayNum]["Temperature"]["Maximum"]["Value"]}°'
              f'/{five_day_forecast[dayNum]["Temperature"]["Minimum"]["Value"]} | '
              f'{five_day_forecast[dayNum]["Day"]["IconPhrase"]}')
        print('--------------------------------------------------------')


def ask_for_location():
    print("Hello there! To get your weather, I'll need your location.")
    while True:
        zip = input("Please enter your postal code:")
        if zip == "" or len(zip) < 5 or (len(zip) > 5 and '-' not in zip):
            print("I'm sorry, that's not a valid zip code. Please try again.")
            continue

        request = requests.get(create_location_url(key, zip))

        if request.status_code != 200:
            if request.status_code == 503:
                raise QuotaReachedError("The api quota has been exceeded. Sorry!")
            raise LocationError("Unable to find your location. Sorry!")

        if request.text == "[]":
            try_somewhere_else = input("We couldn't find your location. Do you want to try a different place? (y or n)") \
                                 == "y"
            if try_somewhere_else:
                continue
            else:
                raise LocationError("ask_for_location: unable to get location, " + request.text)

        # There's more than one location matching the search text. Ask the user which is theirs
        if len(request.json()) > 1:
            print("We found multiple places matching your search query.")
            for value in request.json():
                does_live_there = input(f'Do you live in {value["LocalizedName"]}? (y or n)') == "y"
                if does_live_there:
                    return value["Key"]
            return None


if __name__ == '__main__':
    main()


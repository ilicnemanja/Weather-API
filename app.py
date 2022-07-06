import requests
import configparser
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('settings.ini')

cities = ['Istanbul', 'Moscow', 'London', 'Leningrad', 'Berlin', 'Madrid', 'Kyiv', 
'Rome', 'Bucharest', 'Paris', 'Minsk', 'Sarajevo', 'Banja Luka', 'Vienna', 'Hamburg', 'Warsaw', 'Budapest', 'Belgrade', 
'Barcelona', 'Munich', 'Kharkiv', 'Milan', 'Sofia', 'Skoplje', 'Prague', 'Kazan', 'Nizhny Novgorod', 'Samara',
'Birmingham', 'Rostov-on-Don', 'Ufa', 'Cologne', 'Voronezh', 'Perm', 'Volgograd']


def get_weather(city):
    """
    GET Weather from Foreca Weather API
    https://developer.foreca.com/

    ...

    Parameters
    ----------
    city : str
        City in Europe.

    Returns
    ----------
    data : dict
        Weather for given city.
    """
    
    url = 'https://pfa.foreca.com/api/v1/'
    token = config['API']['token']

    try:
        response1 = requests.get(url=f"{url}location/search/{city}?token={token}")
        data1 = response1.json()

        city_name = data1['locations'][0]['name']
        country = data1['locations'][0]['country']
        timezone = data1['locations'][0]['timezone']
        lon = data1['locations'][0]['lon']
        lat = data1['locations'][0]['lat']
        city_id = data1['locations'][0]['id']

        response2 = requests.get(url=f"{url}forecast/daily/{city_id}?token={token}")
        data2 = response2.json()

        date_formatting = data2['forecast'][0]['date']
        today_date = datetime.strptime(date_formatting, '%Y-%m-%d').strftime('%a, %d. %B')
        symbol = data2['forecast'][0]['symbol']
        maxTemp = data2['forecast'][0]['maxTemp']
        minTemp = data2['forecast'][0]['minTemp']
        maxWindSpeed = data2['forecast'][0]['maxWindSpeed']

        data = {
            "city_name": city_name, "country": country, "timezone": timezone, "lat": lat, "lon": lon, "date": today_date, 
            "maxTemp": maxTemp, "minTemp": minTemp, "symbol": symbol, "maxWindSpeed": maxWindSpeed
        }

        return data

    except TypeError as type_error:
        print(f"Are you sure you entered the city correctly?\nError: {type_error}")
    except IndexError:
        pass
    except Exception as error:
        print(error)

def get_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    return current_time

@app.route("/")
def home():
    return render_template('home.html', cities=cities, current_time=get_time())

@app.route("/<city>", methods=["GET"])
def weather_for_city(city):
    weather = get_weather(city)
    return render_template('city.html', weather=weather, cities=cities, current_time=get_time())

@app.route("/search", methods=["GET"])
def searched_city():
    city = request.args.get('city')
    weather = get_weather(city)

    return render_template('searched_city.html', weather=weather, cities=cities, current_time=get_time())


if __name__ == "__main__":
    app.run(debug=True)


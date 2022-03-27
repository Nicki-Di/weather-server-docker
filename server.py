import hug
from dotenv import dotenv_values
import requests
import socket
import getpass


# Method to read config file settings
def config():
    return dotenv_values(".env")


# Method to response on localhost:8080/
@hug.get('/')
def weather(city: hug.types.text = "Tehran"):
    query = {'query': city, 'access_key': config().get('ACCESS_KEY')}
    response = requests.get(f"{config().get('WEATHER_API')}", params=query)
    response_body = response.json()
    data = {
        "hostname": getpass.getuser() + '@' + socket.gethostname(),
        "temperature": response_body['current']['temperature'],
        "weather_descriptions": response_body['current']['weather_descriptions'][0],
        "wind_speed": response_body['current']['wind_speed'],
        "humidity": response_body['current']['humidity'],
        "feelslike": response_body['current']['feelslike']
    }

    return data


hug.API(__name__).http.serve(port=int(config().get('PORT')))

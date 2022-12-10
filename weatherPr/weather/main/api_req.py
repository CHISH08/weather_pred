import requests
import os
from decouple import config
from geopy.geocoders import Nominatim

appid = config('appid')

def apiWeather_find(post_id):
    url = f'https://api.openweathermap.org/data/2.5/find?q={post_id}&cnt=3&appid={appid}'
    res = requests.get(url).json()['list']
    return res

def apiWeath_get(name):
    return requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={name}&units=metric&appid={appid}').status_code

def apiWeater_weather(name):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={name}&units=metric&appid={appid}'
    res = requests.get(url).json()
    return res

def apiGeopy(name):
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(name)
    loc = [getLoc.longitude, getLoc.latitude]
    return loc
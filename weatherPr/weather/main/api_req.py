import requests
import os
from decouple import config
from geopy.geocoders import Nominatim

appid = config('appid') # Скрытая переменная


# Запрос к api openweathermap: выводит данные о погоде на несколько промежутков в определенном городе
def apiWeather_find(post_id):
    url = f'https://api.openweathermap.org/data/2.5/find?q={post_id}&cnt=3&appid={appid}'
    res = requests.get(url).json()['list']
    return res

# Запрос к api openweathermap: проверяет status_code
def apiWeath_get(name):
    return requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={name}&units=metric&appid={appid}').status_code

# Запрос к api openweathermap: выводит данные о погоде на данный момент в определенном городе
def apiWeater_weather(name):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={name}&units=metric&appid={appid}'
    res = requests.get(url).json()
    return res

# Запрос к api geopy: получение координат определенного города
def apiGeopy(name):
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(name)
    loc = [getLoc.longitude, getLoc.latitude]
    return loc
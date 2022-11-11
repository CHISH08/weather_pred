from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm
from geopy.geocoders import Nominatim

def city_info(request, post_id):
    appid = '001a0b6c43d9a8306b7c701171339c46'
    #url = f'https://api.openweathermap.org/data/2.5/find?q={post_id}&cnt=9&units=metric&appid={appid}'
    #res = requests.get(url).json()['list']
    city = {}

    # for i in range(len(res)):
    #     rs = res[i]
    #     city[str(i * 3)] = {
    #         'city': post_id,
    #         'temp': rs['main']['temp'],
    #         'icon': rs['weather'][0]['icon'],
    #         'feels_like': rs['main']['feels_like'],
    #         'wind_speed': rs['wind']['speed'],
    #         'pressure': rs['main']['pressure'],
    #         'rain': rs['weather'][0]['main']
    #     }

    for i in range(8):
        city[i] = {
            "city": post_id,
            'temp': 25,
            'icon': 'cloud',
            'feels_like': 22,
            'wind_speed': 2,
            'pressure': 1002,
            'rain': 'Rain',
        }
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(post_id)
    loc = [getLoc.longitude, getLoc.latitude]
    context = {
        'city': city,
        'loc': loc,
    }
    return render(request, 'main/city.html', context)

def index(request):
    cit_info = {}
    appid = '08fd3b49c351fe3143d4ab937e60842c'
    city = City.objects.all()
    error = ''
    if request.method == 'POST':
        name = request.POST['name']
        form = CityForm(request.POST)
        flag = True
        if 0: #requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={name}&units=metric&appid={appid}').status_code == 404:
            error = "Данные некорректны!"
        else:
            for cit in city:
                if cit.name == name:
                    flag = False
            if (flag):
                form.save()
            return redirect("inf_city", post_id=name)

    form = CityForm()
    city = City.objects.all()

    for cit in city:
        # url = f'https://api.openweathermap.org/data/2.5/weather?q={cit.name}&units=metric&appid={appid}'
        # res = requests.get(url).json()
        # cit_info[cit.name] = {
        #     'city': cit.name,
        #     'temp': res['main']['temp'],
        #     'icon': res['weather'][0]['icon'],
        #     'feels_like': res['main']['feels_like'],
        #     'wind_speed': res['wind']['speed'],
        #     'pressure': res['main']['pressure'],
        #     'visibility': res['visibility'],
        #     'rain': res['weather'][0]['main'],
        # }
        cit_info[cit.name] = {
            "city": cit.name,
            'temp': 25,
            'icon': 'cloud',
            'feels_like': 22,
            'wind_speed': 2,
            'pressure': 1002,
            'rain': 'Rain',
        }

    context = {
        'info': cit_info,
        'loc': [37.618423, 55.751244],
        'form': form,
        'error': error,
    }

    return render(request, 'main/home.html', context)
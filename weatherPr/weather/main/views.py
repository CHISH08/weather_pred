from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm
from geopy.geocoders import Nominatim
import tensorflow as tf
import numpy as np
from transliterate import translit
import pandas as pd

def wx_input_fn(X, y=None, num_epochs=None, shuffle=True, batch_size=400):
    return tf.compat.v1.estimator.inputs.pandas_input_fn(x=X,
                                               y=y,
                                               num_epochs=num_epochs,
                                               shuffle=shuffle,
                                               batch_size=batch_size)

def city_info(request, post_id):
    appid = '001a0b6c43d9a8306b7c701171339c46'
    url = f'https://api.openweathermap.org/data/2.5/find?q={post_id}&cnt=9&units=metric&appid={appid}'
    res = requests.get(url).json()['list']
    city = {}
    name = translit(post_id, 'ru')

    for i in range(len(res)):
        rs = res[i]
        city[str(i * 3)] = {
            'city': post_id,
            'name': name,
            'temp': rs['main']['temp'],
            'icon': rs['weather'][0]['icon'],
            'feels_like': rs['main']['feels_like'],
            'wind_speed': rs['wind']['speed'],
            'pressure': rs['main']['pressure'],
            'rain': rs['weather'][0]['main']
        }

    # for i in range(8):
    #     city[i] = {
    #         "city": post_id,
    #         'temp': 25,
    #         'icon': 'cloud',
    #         'feels_like': 22,
    #         'wind_speed': 2,
    #         'pressure': 1002,
    #         'rain': 'Rain',
    #     }
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
        name = translit(name, language_code='ru', reversed=True)
        form = CityForm(request.POST)
        flag = True
        if requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={name}&units=metric&appid={appid}').status_code == 404:
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
        ct = cit.name
        cit.name = translit(cit.name, language_code='ru', reversed=True)
        url = f'https://api.openweathermap.org/data/2.5/weather?q={cit.name}&units=metric&appid={appid}'
        res = requests.get(url).json()
        cit_info[cit.name] = {
            'city1': cit.name,
            'city2': ct,
            'temp': res['main']['temp'],
            'icon': res['weather'][0]['icon'],
            'feels_like': res['main']['feels_like'],
            'wind_speed': res['wind']['speed'],
            'pressure': res['main']['pressure'],
            'visibility': res['visibility'],
            'rain': res['weather'][0]['main'],
        }
    # for cit in city:
    #     cit_info[cit.name] = {
    #         "city": cit.name,
    #         'temp': 25,
    #         'icon': 'cloud',
    #         'feels_like': 22,
    #         'wind_speed': 2,
    #         'pressure': 1002,
    #         'rain': 'Rain',
    #     }

    context = {
        'info': cit_info,
        'loc': [37.618423, 55.751244],
        'form': form,
        'error': error,
    }

    return render(request, 'main/home.html', context)

def pred(request, post_id):
    city = {}
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(post_id)
    loc = [getLoc.longitude, getLoc.latitude]
    # url = f'https://api.openweathermap.org/data/2.5/find?q={post_id}&cnt=9&units=metric&appid={appid}'
    # res = requests.get(url).json()['list']
    X = pd.DataFrame(data=np.array([[10 for i in range(36)]]),
                    columns=np.array([str(i) for i in range(36)]))
    feature_cols = [tf.feature_column.numeric_column(col) for col in X.columns]
    regressor = tf.estimator.DNNRegressor(feature_columns=feature_cols,
                                          hidden_units=[50, 50],
                                          model_dir='tf_wx_model')
    pred = regressor.predict(input_fn=wx_input_fn(X,
                                                  num_epochs=1,
                                                  shuffle=False))
    predictions = np.array([p['predictions'][0] for p in pred])
    name = translit(post_id, 'ru')
    for i in range(8):
        city[i] = {
            'city': post_id,
            'name': name,
            'temp': predictions[0],
            'icon': 'cloud',
            'feels_like': 22,
            'wind_speed': 2,
            'pressure': 1002,
            'rain': 'Rain',
        }
    context = {
        'city': city,
        'loc': loc,
    }
    return render(request, 'main/city.html', context)
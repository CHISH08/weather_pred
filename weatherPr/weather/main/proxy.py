from transliterate import translit
import pandas as pd
from .api_req import *
from .pred import *

# Функция, обрабатывающая res и выбирающая из него нужные данные
def make_dat(res):
    dat = np.array([0 for j in range(23)], dtype=float)
    dat[0] = res[0]['coord']['lon']
    dat[1] = res[0]['coord']['lat']
    j = 2
    for rs in reversed(res):
        dat[j + 3] = rs['main']['temp_min']
        dat[j + 6] = rs['main']['temp_max']
        dat[j + 9] = rs['main']['pressure']
        dat[j + 12] = rs['main']['pressure']
        dat[j + 15] = rs['main']['humidity']
        dat[j + 18] = rs['wind']['speed']
        dat[j] = rs['main']['temp']
        j += 1

    counter1 = 0
    counter2 = 0
    i = 3
    j = 4
    while i < len(dat):
        if dat[i] == 0:
            counter1 += 1
        i += 3
    while j < len(dat):
        if dat[j] == 0:
            counter2 += 1
        j += 3
    if (counter1 == 7):
        j = 3
        while j < len(dat):
            dat[j] = dat[j - 1]
            j += 3
    if (counter2 == 7):
        j = 4
        while j < len(dat):
            dat[j] = dat[j - 1]
            j += 3

    if (dat[21] == 0):
        dat[21] = 0.5
    if (dat[22] == 0):
        dat[22] = 0.5

    return np.array([dat])

# Подается название города и по названию ищутся нужные нам данные(прогноз на сегодняшний день) по этому городу,
# которые возвращаются в city_info
def proxy_city_info(post_id):
    loc = apiGeopy(post_id)
    rs = apiWeather_find(post_id)[0] # Обращение к api openweather
    name = translit(post_id, 'ru')
    city = {
        'city': post_id,
        'name': name,
        'type': "Сегодня",
        'url': "pred",
        'temp': round(rs['main']['temp'] - 273.15),
        'icon': rs['weather'][0]['icon'],
        'feels_like': round(rs['main']['feels_like'] - 273.15),
        'wind_speed': round(rs['wind']['speed'],1),
        'pressure': round(rs['main']['pressure']),
        'rain': rs['weather'][0]['main']
    }
    context = {
        'city': city,
        'loc': loc,
    }
    return context

# Подается названия городов и по названиям ищутся нужные нам данные
# (прогноз на сегодняшний день) по этим городам,
# которые возвращаются в index
def proxy_index(city, form, error):
    cit_info = {}
    for cit in city:
        ct = cit.name
        cit.name = translit(cit.name, language_code='ru', reversed=True)
        res = apiWeater_weather(cit.name)
        cit_info[cit.name] = {
            'city1': cit.name,
            'city2': ct,
            'temp': round(res['main']['temp']),
            'icon': res['weather'][0]['icon'],
            'feels_like': round(res['main']['feels_like']),
            'wind_speed': round(res['wind']['speed'],1),
            'pressure': round(res['main']['pressure']),
            'visibility': res['visibility'],
            'rain': res['weather'][0]['main'],
        }

    context = {
        'info': cit_info,
        'loc': [37.618423, 55.751244],
        'form': form,
        'error': error,
    }
    return context

# Подается название города и по названию ищутся нужные нам данные
# (прогноз на несколько промежутков сегодняшнего дня) по этому городу,
# которые обрабатываются, подаются в нейронную сеть и результат отправляется в pred
def proxy_pred(post_id):
    loc = apiGeopy(post_id)
    res = apiWeather_find(post_id)
    name = translit(post_id, 'ru')

    X = pd.DataFrame(data=make_dat(res),
                     columns=np.array([str(j) for j in range(23)]))

    X = X.rename(columns={'0': 'lon', '1': 'lat', '2': 'temp_1', '3': 'temp_2', '4': 'temp_3',
                          '5': 'temp_min_1', '6': 'temp_min_2', '7': 'temp_min_3', '8': 'temp_max_1',
                          '9': 'temp_max_2', '10': 'temp_max_3', '11': 'pressure_1', '12': 'pressure_2',
                          '13': 'pressure_3', '14': 'sea_level_1', '15': 'sea_level_2', '16': 'sea_level_3',
                          '17': 'humidity_1', '18': 'humidity_2', '19': 'humidity_3', '20': 'speed_1',
                          '21': 'speed_2', '22': 'speed_3'})
    feature_cols = [tf.feature_column.numeric_column(col) for col in X.columns]

    temp = NN_pred(X, "pred/Temp_model", feature_cols).pred() - 273.15
    # hum = NN_pred(X, "Hum_model", feature_cols)
    wind_speed = NN_pred(X, "pred/Wind_model", feature_cols).pred()
    pres = NN_pred(X, "pred/Pres_model", feature_cols).pred()
    city = {
        'city': post_id,
        'name': name,
        'temp': round(temp),
        'type': "Предсказание",
        'url': "inf_city",
        'icon': 'norm',
        'feels_like': round(13.12 + 0.6215 * temp - 11.37 * (wind_speed * 1.5) ** (0.16) + 0.3965 * temp * (wind_speed * 1.5) ** (0.16)),
        'wind_speed': round(wind_speed, 1),
        'pressure': round(pres),
        'rain': 'norm',
    }
    context = {
        'city': city,
        'loc': loc,
    }

    return context
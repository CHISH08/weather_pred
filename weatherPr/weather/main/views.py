from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm
from .proxy import *

# Функция, занимающаяся подачей данных на страницу описания погоды в определнном городе
def city_info(request, post_id):
    context = proxy_city_info(post_id)
    return render(request, 'main/city.html', context)

# Функция, занимающаяся подачей данных на главную страницу и обработкой поданных данных в него для отправки в БД
def index(request):
    city = City.objects.all()
    error = ''
    if request.method == 'POST':
        name = request.POST['name']
        name = translit(name, language_code='ru', reversed=True)
        form = CityForm(request.POST)
        flag = True
        if apiWeath_get(name) == 404:
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

    context = proxy_index(city, form, error)

    return render(request, 'main/home.html', context)

# Функция, занимающаяся подачей данных на страницу с предсказаниями погоды в определенном городе
def pred(request, post_id):
    context = proxy_pred(post_id)
    return render(request, 'main/city.html', context)
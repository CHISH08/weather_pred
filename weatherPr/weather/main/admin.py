from django.contrib import admin
from .models import City

# Регистрирует в БД class City(Порожденный class от django.db.models.Models)
admin.site.register(City)
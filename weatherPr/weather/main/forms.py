from .models import City
from django.forms import ModelForm, TextInput

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name': TextInput(attrs={
            'id': 'city',
            'name': 'city',
            'type': "search",
            'class': "form-control form-control-dark text-bg-dark",
            'placeholder': "Введите город...",
            'aria-label': "Search"
        })}
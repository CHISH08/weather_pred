from django.db import models
from django.urls import reverse

# class City(Порожденный class от django.db.models.Models): описывает какие группы подаются в БД
class City(models.Model):
    name = models.CharField(max_length=30)

    def __srt__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.name})
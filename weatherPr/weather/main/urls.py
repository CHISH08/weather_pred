from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('<slug:post_id>/', views.city_info, name='inf_city'),
    path('<slug:post_id>/predict', views.pred, name='pred'),
]
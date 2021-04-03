from django.urls import path

from core import ajax_views as views

app_name = 'core'

urlpatterns = [
    path('players', views.players, name="players"),
]

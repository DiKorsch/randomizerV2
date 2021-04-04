from django.urls import path

from core import ajax_views as views

app_name = 'core'

urlpatterns = [
    path('players', views.players, name="players"),
    path('heartbeat', views.heartbeat, name="heartbeat"),
    path('randomize', views.Randomize.as_view(), name="randomize"),
]

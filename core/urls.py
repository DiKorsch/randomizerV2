from django.urls import path

from core import views

urlpatterns = [

    path('', views.IndexView.as_view(), name="index"),
    path('clear', views.IndexView.clear_cookie, name="clear_cookie"),
]

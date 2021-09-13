from django.urls import path
from . import views
#39:45 Para meter la aplicación de dash_apps:
from home.dash_apps.finished_apps import simpleexample
from home.dash_apps.finished_apps import evolution

#IMPORTANTE ACORDARNOS DE IMPORTAR CUANDO METAMOS MÁS GRAFICOS. Luego vamos a partials-base.html 40:22

urlpatterns = [
    path('', views.home, name='home')
]


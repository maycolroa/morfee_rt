from django.urls import path
from . import views

urlpatterns = [
    path('prueba', views.tpl_prueba, name='us_prueba'),
]

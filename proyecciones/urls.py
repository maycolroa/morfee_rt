from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.tpl_inicio, name='pro_inicio'),
    path('predecir', views.predecir, name='pro_predecir'),
    path('chat', views.tpl_chat, name='pro_chat'),
]

from django.urls import path, include
from . import views

urlpatterns = [
    path('dash/consulta/auto', views.getConsulta, name='retec_consulta'),
]

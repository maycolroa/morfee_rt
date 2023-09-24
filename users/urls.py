from django.urls import path
from . import views

urlpatterns = [
    path('prueba', views.tpl_prueba, name='us_prueba'),
    path('admin/history/import', views.import_history, name='ad_history_import'),
]

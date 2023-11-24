from django.urls import path
from . import views

urlpatterns = [
    path('santiago', views.tpl_santiago),
    path('xml', views.tpl_xml),
]


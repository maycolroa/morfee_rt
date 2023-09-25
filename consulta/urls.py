from django.urls import path, include
from . import views

urlpatterns = [
    path('dash/consulta/auto', views.getConsulta, name='retec_consulta'),
    path('consultas_view',views.consultas_view),
    path('slice/data', views.slice_data, name='retec_slice'),
]

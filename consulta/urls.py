from django.urls import path, include
from . import views

urlpatterns = [
    path('dash/consulta/auto', views.getConsulta, name='retec_consulta'),
    path('consultas_view',views.consultas_view),
    path('slice/data', views.slice_data, name='retec_slice'),
    path('facturas/prestadores', views.fac_prestadores),
    path('pagos/prestadores', views.pay_prestadores),
    path('load', views.loadConsulta),   # Invoke reserva_global
    path('save', views.saveConsulta, name='search_save')
]

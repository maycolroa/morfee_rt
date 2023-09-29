from django.urls import path, include
from . import views

urlpatterns = [
    path('piramide', views.piramide, name='retec_piramide'),
    path('piramide/data', views.pyr_data, name='retec_pyr_data'),
    path('mng/view/summary', views.mng_view, name='retec_view'),
    path('mng/data/fuente', views.mng_fuente_pyr, name='retec_fuente'),

    path('reserva', views.tpl_reserva, name='try_reserva'),
]

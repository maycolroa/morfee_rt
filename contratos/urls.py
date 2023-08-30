from django.urls import path, include
from . import views

urlpatterns = [
    path('contratos/<str:section>/', views.cont_panel, name='retec_contratos'),
    path('dash/contratos', views.dash_contratos, name='retec_contratos_new'),
    path('dash/contratos/data', views.raw_facet, name='retec_con_data'),
    path('dash/contratos/schema', views.schema_contrato, name='retec_con_sch'),
]

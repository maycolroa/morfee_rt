from django.urls import path, include
from . import views

urlpatterns = [
    path('facturas/<str:section>/', views.fac_panel, name='retec_facturas'),
    path('cuentas/medicas', views.tpl_cuentas_medicas, name='fac_cm'),
    path('dash/facturas', views.dash_facturas, name='retec_facturas_new'),
    path('dash/facturas/data', views.raw_facet_fac, name='retec_facturas_data'),
    path('dash/facturas/controls', views.raw_facet_fac_control, name='retec_facturas_ctr'),
    path('dash/facturas/indigena', views.raw_facet_fac_indi, name='retec_facturas_indi'),
    path('dash/facturas/schema', views.schema_factura, name='retec_facturas_sch'),

    path('cuentas/medicas/data', views.data_cm, name='fac_cm_data'),
]

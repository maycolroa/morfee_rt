from django.urls import path, include
from . import views

urlpatterns = [
    path('pagos/<str:section>/', views.pag_panel, name='retec_pagos'),
    path('dash/pagos', views.dash_pagos, name='retec_pagos_new'),
    path('dash/pagos/data', views.raw_facet_pay, name='retec_pagos_data'),
    path('dash/pagos/controls', views.raw_facet_pay_control, name='retec_pagos_ctr'),
    path('dash/pagos/schema', views.schema_pago, name='retec_pago_sch'),
    path('cuentas/medicas', views.tpl_cuentas_medicas, name='pag_cm'),

    path('cuentas/medicas/data', views.data_cm, name='pag_cm_data'),
]

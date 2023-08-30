from django.urls import path, include
from . import views

urlpatterns = [
    path('pagos/<str:section>/', views.pag_panel, name='retec_pagos'),
    path('dash/pagos', views.dash_pagos, name='retec_pagos_new'),
    path('dash/pagos/data', views.raw_facet_pay, name='retec_pagos_data'),
    path('dash/pagos/controls', views.raw_facet_pay_control, name='retec_pagos_ctr'),
    path('dash/pagos/schema', views.schema_pago, name='retec_pago_sch'),
]

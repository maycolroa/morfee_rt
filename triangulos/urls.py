from django.urls import path, include
from . import views

urlpatterns = [
    path('piramide', views.piramide, name='retec_piramide'),
    path('piramide/data', views.pyr_data, name='retec_pyr_data'),

    path('mng/view/summary', views.mng_view, name='retec_view'),
    path('mng/data/fuente', views.mng_fuente_pyr, name='retec_fuente'),

    # path('dashboards/<str:section>/', views.dashboards, name='retec_dashboard'),
    # path('contratos/<str:section>/', views.cont_panel, name='retec_contratos'),
    # path('facturas/<str:section>/', views.fac_panel, name='retec_facturas'),
    # path('pagos/<str:section>/', views.pag_panel, name='retec_pagos'),
    # path('incapacidades/<str:section>/', views.inca_panel, name='retec_incapacidades'),
    # path('fragmentacion', views.fragmentation, name='retec_fragment'),
    # path('info/periodos', views.getPeriodos, name='retec_periodos'),
    # path('info/orphan', views.getCreatedOrphan, name='retec_orphan'),
    # path('mng/facet', views.mng_facet, name='retec_mng_facet'),
    # path('mng/group', views.mng_group, name='retec_mng_group'),
    # path('mng/group/multiple', views.mng_group_multiple, name='retec_mng_group_multiple'),
    # path('mng/schema', views.mng_schema, name='retec_mng_schema'),
    # path('mng/distinct', views.mng_distinct, name='retec_distinct'),
    # path('mng/fixed/crx', views.fixedPeriodo, name='retec_mng_crx'),

    # path('dash/contratos', views.dash_contratos, name='retec_contratos_new'),
    # path('dash/contratos/data', views.raw_facet, name='retec_con_data'),
    # path('dash/contratos/schema', views.schema_contrato, name='retec_con_sch'),

    
    # path('dash/facturas', views.dash_facturas, name='retec_facturas_new'),
    # path('dash/facturas/data', views.raw_facet_fac, name='retec_facturas_data'),
    # path('dash/facturas/controls', views.raw_facet_fac_control, name='retec_facturas_ctr'),
    # path('dash/facturas/indigena', views.raw_facet_fac_indi, name='retec_facturas_indi'),
    # path('dash/facturas/schema', views.schema_factura, name='retec_facturas_sch'),

    # path('dash/pagos', views.dash_pagos, name='retec_pagos_new'),
    # path('dash/pagos/data', views.raw_facet_pay, name='retec_pagos_data'),
    # path('dash/pagos/controls', views.raw_facet_pay_control, name='retec_pagos_ctr'),
    # path('dash/pagos/schema', views.schema_pago, name='retec_pago_sch'),

    # path('dash/incapacidades', views.dash_incapacidades, name='retec_incapacidades_new'),
    # path('dash/incapacidades/data', views.raw_facet_inca, name='retec_incapacidades_data'),
    # path('dash/incapacidades/schema', views.schema_inca, name='retec_inca_sch'),

    # path('dash/consulta/auto', views.getConsulta, name='retec_consulta'),
    
    # # reservas/mng/group
    # path('slice/data', views.slice_data, name='retec_slice'),

    # path('mng/raw', views.raw_facet, name='retec_raw'),
]

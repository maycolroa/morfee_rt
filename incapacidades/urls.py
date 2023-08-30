from django.urls import path, include
from . import views

urlpatterns = [
    path('incapacidades/<str:section>/', views.inca_panel, name='retec_incapacidades'),
    path('dash/incapacidades', views.dash_incapacidades, name='retec_incapacidades_new'),
    path('dash/incapacidades/data', views.raw_facet_inca, name='retec_incapacidades_data'),
    path('dash/incapacidades/schema', views.schema_inca, name='retec_inca_sch'),
]

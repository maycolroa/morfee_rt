from django.urls import path
from . import views

urlpatterns = [
    path('prueba', views.tpl_prueba, name='us_prueba'),
    path('admin/history/import', views.import_history, name='ad_history_import'),
    #lista de frontier
    path('admin/users', views.user_list, name='ad_user_list'),
    path('admin/user/select', views.user_preselect, name='ad_user_preselect'),
    path('admin/user/edit/<int:id>/', views.user_edit, name='ad_user_edit'),
    path('admin/user/add', views.user_add, name='ad_user_add'),
    path('admin/user/add/staff', views.user_add_staff, name='ad_user_add_staff'),
    path('admin/user/remove/<int:id>/', views.user_remove, name='ad_user_remove'),
    


    #fin frontier

]

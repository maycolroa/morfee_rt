"""
URL configuration for morfee_rt_dev project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.CustomLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password_change/', views.CustomChangePWDView.as_view(template_name='users/password_change_form.html'), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),

    path('autorizaciones/', include('autorizaciones.urls')),
    path('contratos/', include('contratos.urls')),
    path('facturas/', include('facturas.urls')),
    path('incapacidades/', include('incapacidades.urls')),
    path('pagos/', include('pagos.urls')),
    path('consulta/', include('consulta.urls')),
    path('proyecciones/', include('proyecciones.urls')),
    path('triangulos/', include('triangulos.urls')),
    path('users/', include('users.urls'))
]

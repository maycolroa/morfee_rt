from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from . import forms

class CustomLoginView(LoginView):
    authentication_form = forms.CustomAuthenticationForm

class CustomChangePWDView(PasswordChangeView):
    form_class = forms.CustomPasswordChangeForm

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/login/')
def inicio(request):
    modulos = []
    return render(request, 'base/inicio.html', {'modulos': modulos, 'cantidad': len(modulos)})


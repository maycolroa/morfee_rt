from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from . import forms, models
from time import sleep
import json, datetime
# Create your views here.

def tpl_prueba(request):
    sleep(5)
    return render(request, 'users/prueba.html')

def date_to_string(fl):
    if isinstance(fl, datetime.date):
        return fl.isoformat()

def import_history(request):
    if request.method == 'POST':
        colec = request.POST.get('coleccion')
        print(colec)
        datos = models.ControlImportBasic.objects.filter(coleccion=colec).values('id', 'coleccion', 'created_at', 'total')
        lista = list(datos)
        rs = json.dumps(lista, default=date_to_string)
        return HttpResponse(rs, content_type="application/json")
    else:
        return JsonResponse([], content_type="application/json")

from django.shortcuts import render
from time import sleep
# Create your views here.

def tpl_prueba(request):
    sleep(5)
    return render(request, 'users/prueba.html')
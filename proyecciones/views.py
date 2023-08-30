from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from morfee_rt_dev.mongo import Mongo
import json
# from bson.code import Code

@login_required(login_url='/login/')
def tpl_inicio(request):
    return render(request, 'proyecciones/inicio.html')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from morfee_rt_dev.mongo import Mongo
from morfee_rt_dev import settings
import tensorflow as tf
import pandas as pd
import numpy as np
# from sklearn.externals import joblib
import joblib
import json
import os
# from bson.code import Code

@login_required(login_url='/login/')
def tpl_inicio(request):
    return render(request, 'proyecciones/inicio.html')

def predecir(request):
    model_file = os.path.join(settings.MODELS, 'dl_rt_pagos.h5')
    model = tf.keras.models.load_model(model_file)
    # model.summary()
    content = {
        'ï»¿IdPrestador': int(request.POST.get('prestador')), 
        'planSalud': int(request.POST.get('plansalud')), 
        'TContra': int(request.POST.get('tcontra')), 
        'Ambito': int(request.POST.get('ambito')), 
        'FPres': int(request.POST.get('fpres')), 
        'FRad': int(request.POST.get('frad')), 
        'GlosaDefinitiva': int(request.POST.get('glosadefinitiva')), 
        'MecPago': int(request.POST.get('mecpago')), 
        'VlrPagadoPBS': int(request.POST.get('pbs')), 
        'VlrPagadoPAC': int(request.POST.get('pac')), 
        'VlrPagadoPM': int(request.POST.get('pm')), 
        'FPago': int(request.POST.get('fpago')), 
        'pres_Max': int(request.POST.get('pres')), 
        'Covid': int(request.POST.get('covid'))
    }
    print(content)
    rs = pd.DataFrame([content])
    x = rs[['ï»¿IdPrestador', 'planSalud', 'TContra', 'Ambito', 'FPres', 'FRad', 'MecPago', 'FPago', 'pres_Max', 'Covid', 'GlosaDefinitiva', 'VlrPagadoPBS', 'VlrPagadoPAC', 'VlrPagadoPM']]
    prediction = model.predict(x)
    dato = str(prediction[0][0])
    return JsonResponse({'status': 'success', 'resultado': dato}, safe=False)

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Consulta
from datetime import date
from morfee_rt_dev.mongo import Mongo
import json

# Create your views here.
def getConsulta(request):
    keycode = str(request.POST.get('clave')) if request.POST.get('clave') else ''
    name = request.POST.get('consulta')
    uid = request.user.id
    print('Claving: ' + keycode + ', consulting: ' + name)
    c = Consulta.objects.filter(nombre=name, clave=keycode).first() if keycode != '' else Consulta.objects.filter(nombre=name).first()
    if c:
        contenido = json.loads(c.contenido) if c.contenido else []
        print('Consulta encontrada')
        rs = {'nombre': c.nombre, 'coleccion': c.coleccion, 'contenido': contenido, 'clave': c.clave, 'estado': c.estado, 'created_at': c.created_at}
        return JsonResponse(rs)
    else:
        print('No existe la consulta')
        rs = {'nombre': name, 'coleccion': '', 'contenido': '', 'clave': keycode, 'estado': 'void', 'created_at': str(date.today())}
        return JsonResponse(rs)
    
    # try:
    #     # c = Consulta.objects.filter(nombre=name, clave=keycode, user_id=uid).get() if keycode != '' else Consulta.objects.filter(nombre=name, user_id=uid).get()
    #     c = Consulta.objects.filter(nombre=name, clave=keycode).first() if keycode != '' else Consulta.objects.filter(nombre=name).first()
    #     print('dona')
    #     print(c)
    #     contenido = json.loads(c.contenido) if c.contenido else []
    #     print('Consulta encontrada')
    #     rs = {'nombre': c.nombre, 'coleccion': c.coleccion, 'contenido': contenido, 'clave': c.clave, 'estado': c.estado, 'created_at': c.created_at}
    #     return JsonResponse(rs)
    # except Consulta.DoesNotExist:
    #     print('No existe la consulta')
    #     rs = {'nombre': name, 'coleccion': '', 'contenido': '', 'clave': keycode, 'estado': 'void', 'created_at': str(date.today())}
    #     return JsonResponse(rs)

def createConsulta(name, cole, cla, user):
    print('Generando consulta: ' + name)
    try:
        # c = Consulta.objects.filter(nombre=name, coleccion=cole, cliente_id=0, user_id=user).get()
        c = Consulta.objects.filter(nombre=name, coleccion=cole, cliente_id=0).get()
        c.clave = cla
        c.estado = 'reopen'
        c.created_at = date.today()
        c.save()
        return c
    except Consulta.DoesNotExist:
        cn = Consulta()
        cn.nombre = name
        cn.coleccion = cole
        cn.clave = cla
        cn.estado = 'open'
        cn.cliente_id = 0
        cn.user_id = user
        cn.save()
        return cn

def consultas_view(request):
    #autorizaciones facturas pagos incapacidades
    cm_colection = request.POST.get('collections') if request.POST.get('collections') else ''
    #datos ={}
    x = []
    if cm_colection != '':
        cm_colection = cm_colection + '_view'
        #verificamos la existencia de la coleccion o view
        mongo_v = Mongo()
        listaCM = mongo_v.listarColecciones()
        query = []
        if cm_colection in listaCM:
            mongo = Mongo(cm_colection)
            x = mongo.aggregate([{'$match':{}}])      
            #datos ={"estado" : "si", "datos":x, "view":cm_colection}
        else:
            x = {'_id':'sin registro'}
            #datos = {'estado' : 'no', 'datos':'', 'view': 'no_exite_view_'+cm_colection}
    else: 
        x = {'_id':'no hay datos'}
        #datos ={'estado' : 'no', 'datos':'', 'view':'no ha enviado coleccion'}
    return HttpResponse(x, content_type="application/json")
    #return JsonResponse(datos)

def slice_data(request):
    coleccion = request.POST.get('coleccion')
    campos = request.POST.get('campos')
    pagina = int(request.POST.get('pagina'))
    cantidad = int(request.POST.get('cantidad'))
    salto = cantidad * (pagina - 1)
    project = {cmp:1 for cmp in campos.split(',')}
    project['_id'] = 0
    rawper = int(request.POST.get('periodo'))
    filtros = request.POST.get('filtros')       # field:value | field:value
    periodo = {"$exists": False} if rawper == 0 else rawper
    match = {'crx': periodo}
    print('canton')
    print(coleccion)
    print(salto)
    print(cantidad)
    print(filtros)
    for fil in filtros.split('|'):
        # field : value : bool
        par = fil.split(':')
        if par[1] == 'exists':
            bool = True if par[2] == 'true' else False
            match[par[0]] = {"$exists": bool}
        else:
            match[par[0]] = par[1]
    mongo = Mongo(coleccion)
    print(match)
    datos = mongo.aggregate([
        {'$match': match},
        {'$project': project },
        {'$skip': salto},
        {'$limit': cantidad + 1}
    ])
    print(datos)
    return HttpResponse(datos, content_type="application/json")

def fac_prestadores(request):
    prestador = request.POST.get('prestador')
    mongo = Mongo('retec_facturas')
    print('kiloe')
    datos = mongo.aggregate([
        {"$project": {'_id':0, 'nmp': 1}},
        {"$match": {"nmp": {"$regex": str(prestador), "$options": "i"}}},
        {"$group": {'_id': "$nmp"}},
        {"$sort": {"nmp": 1}},
        {"$limit": 10}
    ])
    print(datos)
    return HttpResponse(datos, content_type="application/json")

def pay_prestadores(request):
    prestador = request.POST.get('prestador')
    mongo = Mongo('retec_pagos')
    datos = mongo.aggregate([
        {"$project": {'nmp': 1}},
        {"$match": {"nmp": {"$regex": str(prestador), "$options": "i"}}},
        {"$sort": {"nmp": 1}},
        {"$limit": 10}
    ])
    return HttpResponse(datos, content_type="application/json")

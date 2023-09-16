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
    try:
        c = Consulta.objects.filter(nombre=name, clave=keycode, user_id=uid).get() if keycode != '' else Consulta.objects.filter(nombre=name, user_id=uid).get()
        contenido = json.loads(c.contenido) if c.contenido else []
        print('Consulta encontrada')
        rs = {'nombre': c.nombre, 'coleccion': c.coleccion, 'contenido': contenido, 'clave': c.clave, 'estado': c.estado, 'created_at': c.created_at}
        return JsonResponse(rs)
    except Consulta.DoesNotExist:
        print('No existe la consulta')
        rs = {'nombre': name, 'coleccion': '', 'contenido': '', 'clave': keycode, 'estado': 'void', 'created_at': str(date.today())}
        return JsonResponse(rs)

def createConsulta(name, cole, cla, user):
    print('Generando consulta: ' + name)
    try:
        c = Consulta.objects.filter(nombre=name, coleccion=cole, cliente_id=0, user_id=user).get()
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

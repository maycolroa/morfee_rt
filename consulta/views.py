from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Consulta
from datetime import date
from morfee_rt_dev.mongo import Mongo
import json

# Create your views here.
def getConsulta(request):
    keycode = request.POST.get('clave') if request.POST.get('clave') else ''
    name = request.POST.get('consulta')
    cli = request.user.cliente_id if request.user.cliente_id else 0
    uid = request.user.id
    print('Clave: ' + keycode + ', consulta: ' + name)
    try:
        c = Consulta.objects.filter(nombre=name, clave=keycode, cliente_id=cli, user_id=uid).get() if keycode != '' else Consulta.objects.filter(nombre=name, cliente_id=cli, user_id=uid).get()
        contenido = json.loads(c.contenido) if c.contenido else []
        print('Consulta encontrada')
        rs = {'nombre': c.nombre, 'coleccion': c.coleccion, 'contenido': contenido, 'clave': c.clave, 'estado': c.estado, 'created_at': c.created_at}
        return JsonResponse(rs)
    except Consulta.DoesNotExist:
        print('No existe la consulta')
        rs = {'nombre': name, 'coleccion': '', 'contenido': '', 'clave': keycode, 'estado': 'void', 'created_at': str(date.today())}
        return JsonResponse(rs)

def consultas_view(request):
    #autorizaciones facturas pagos incapacidades
    cm_colection = request.POST.get('colections') if request.POST.get('colections') else ''
    datos =[]
    if cm_colection != '':
        cm_colection = cm_colection+'_view' 
        #verificamos la existencia de la coleccion o view
        mongo_v = Mongo()
        listaCM = mongo_v.listarColecciones()
        if cm_colection in listaCM:
            mongo = Mongo(cm_colection).find('')       
            datos =[{'estado' : 'si', 'datos':mongo, 'view':cm_colection}]
        else:
            datos = [{'estado' : 'no', 'datos':'', 'view': 'no_exite_view_'+cm_colection}]
    else:
        datos =[{'estado' : 'no', 'datos':'', 'view':'no ha enviado coleccion'}]
    return HttpResponse(datos, content_type="application/json")




     

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from morfee_rt_dev.mongo import Mongo
from consulta.models import Consulta
from consulta.views import createConsulta, getConsulta
from datetime import date
import json
# from bson.code import Code

def inca_panel(request, section):
    if section == 'inicio':
        return inca_inicio(request)
    elif section == 'table':
        return inca_table(request)
    elif section == 'import':
        return inca_import(request)
    elif section == 'dash':
        return inca_dash(request)

def inca_inicio(request):
    return render(request, 'incapacidades/inca_inicio.html')

def inca_table(request):
    coleccion = 'retec_incapacidades_' + str(request.user.cliente.id) if request.user.cliente else 'retec_incapacidades_0'
    return render(request, 'incapacidades/inca_table.html', {'coleccion': coleccion})

def inca_import(request):
    coleccion = 'retec_incapacidades_' + str(request.user.cliente.id) if request.user.cliente else 'retec_incapacidades_0'
    return render(request, 'incapacidades/inca_import.html', {'coleccion': coleccion})

def inca_dash(request):
    coleccion = 'retec_incapacidades_' + str(request.user.cliente.id) if request.user.cliente else 'retec_incapacidades_0'
    mongo = Mongo(coleccion)
    datos = mongo.aggregate([
        {"$facet": {
            'facet_tpa': [{"$sortByCount": "$tpa"}],
            'facet_total': [{"$group": {"_id": None, "n": {"$sum": 1}}}],
            'facet_vva': [{"$group": {"_id": None, "n": {"$sum": "$vva"}}}],
            'facet_vdo': [{"$group": {"_id": None, "n": {"$sum": "$vdo"}}}],
        }},
    ])
    return HttpResponse(datos, content_type="application/json")

def raw_facet_inca(request):
    tema = request.POST.get('tema') if request.POST.get('tema') else 'retec_incapacidades_0'
    clave = request.POST.get('clave') if request.POST.get('clave') else ''
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    user_id = request.user.id
    consulta = createConsulta('raw_inca_dat' + str(rawper), tema, clave, user_id)
    rs0 = {'$group': {'_id': None, 'total': {'$sum': 1}, 'reserva': {'$sum': '$vva'}, 'pagado': {'$sum': '$vdo'}}}
    if tema == 'retec_incapacidades_0':
        rs0 = {'$group': {'_id': None, 'total': {'$sum': 1}, 'reserva': {'$sum': '$vlri'}, 'pagado': {'$sum': '$vlrp'}}}
    mongo = Mongo(tema)
    try:
        datos = mongo.aggregate([
            {'$match': {'crx': periodo}}, 
            {'$facet': {
                'rs_0': [rs0],
                'rs_1': [{'$group': {'_id': '$tus', 'total': {'$sum': 1}} }],
                'rs_2': [{'$group': {'_id': '$tpa', 'total': {'$sum': 1}} }],
                'tem': [{'$group': {'_id': '$tem', 'total': {'$sum': 1}} }],
                'taf': [{'$group': {'_id': '$taf', 'total': {'$sum': 1}} }],
                'esp': [{'$group': {'_id': '$esp', 'total': {'$sum': 1}} }],
                'tgo': [{'$group': {'_id': '$tgo', 'total': {'$sum': 1}} }],
            }}
        ])
        consulta.contenido = str(datos)
        consulta.estado = 'close'
        consulta.save()
        return HttpResponse(datos, content_type="application/json")
    except:
        consulta.estado = 'failed'
        consulta.save()
        return HttpResponse([], content_type="application/json")

@login_required(login_url='/login/')
def dash_incapacidades(request):
    clienteId = '0'
    cliente = 'NUEVO CLIENTE'
    if request.user.cliente:
        clienteId = request.user.cliente.id
        cliente = request.user.cliente.cliente
    return render(request, 'incapacidades/new_incapacidades.html', {'clienteId': clienteId, 'cliente': cliente})

def schema_inca(request):
    tema = request.POST.get('tema') if request.POST.get('tema') else 'retec_incapacidades_0'
    clave = request.POST.get('clave') if request.POST.get('clave') else ''
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    user_id = request.user.id
    consulta = createConsulta('schema_inca' + str(rawper), tema, clave, user_id)
    mongo = Mongo(tema)
    try:    
        datos = mongo.aggregate([
            {"$match": {'crx': periodo} },
            {'$group': {
                '_id': None,
                'n_tem': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tem', None] }, None] }, 0, 1] } },
                'n_iem': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$iem', None] }, None] }, 0, 1] } },
                'n_tus': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tus', None] }, None] }, 0, 1] } },
                'n_ius': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ius', None] }, None] }, 0, 1] } },
                'n_taf': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$taf', None] }, None] }, 0, 1] } },
                'n_ipa': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ipa', None] }, None] }, 0, 1] } },
                'n_tpa': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tpa', None] }, None] }, 0, 1] } },
                'n_dia': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$dia', None] }, None] }, 0, 1] } },
                'n_cov': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$cov', None] }, None] }, 0, 1] } },
                'n_fip': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$fip', None] }, None] }, 0, 1] } },
                'n_ffp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ffp', None] }, None] }, 0, 1] } },
                'n_sal': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$sal', None] }, None] }, 0, 1] } },
                'n_frp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$frp', None] }, None] }, 0, 1] } },
                'n_esp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$esp', None] }, None] }, 0, 1] } },
                'n_fpa': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$fpa', None] }, None] }, 0, 1] } },
                'n_ds': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ds', None] }, None] }, 0, 1] } },
                'n_tgo': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tgo', None] }, None] }, 0, 1] } },
                'n_vva': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vva', None] }, None] }, 0, 1] } },
                'n_vdo': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vdo', None] }, None] }, 0, 1] } },
                'total': {'$sum': 1}
            }},
        ])
        consulta.contenido = str(datos)
        consulta.estado = 'close'
        consulta.save()
        print(datos)
        return HttpResponse(datos, content_type="application/json")
    except:
        consulta.estado = 'failed'
        consulta.save()
        return HttpResponse([], content_type="application/json")

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from morfee_rt_dev.mongo import Mongo
from consulta.views import createConsulta, getConsulta
from datetime import date

# Create your views here.
def aut_panel(request, section):
    if section == 'inicio':
        return aut_inicio(request)
    elif section == 'table':
        return aut_table(request)
    elif section == 'import':
        return aut_import(request)
    elif section == 'dash':
        return aut_dash(request)

def aut_inicio(request):
    coleccion = 'retec_autorizacion_' + str(request.user.cliente.id) if request.user.cliente else 'retec_autorizacion_0'
    return render(request, 'autorizaciones/aut_inicio.html', {'coleccion': coleccion})

def aut_table(request):
    coleccion = 'retec_autorizacion_' + str(request.user.cliente.id) if request.user.cliente else 'retec_autorizacion_0'
    return render(request, 'autorizaciones/aut_table.html', {'coleccion': coleccion})

def aut_import(request):
    coleccion = 'retec_autorizacion_' + str(request.user.cliente.id) if request.user.cliente else 'retec_autorizacion_0'
    return render(request, 'autorizaciones/aut_import.html', {'coleccion': coleccion})

def aut_dash(request):
    mongo = Mongo('retec_autorizaciones')
    datos = mongo.aggregate([
        {"$facet": {
            'facet_amb': [{"$sortByCount": "$amb"}],
            'facet_pla': [{"$sortByCount": "$pla"}],
            'facet_total': [{"$group": {"_id": None, "n": {"$sum": 1}}}],
            'facet_vbs': [{"$project": {"_id": 0, "n_vbs": {"$convert": {"input": "$vbs", "to": "double", "onError": 0, "onNull": 0}}}}, {"$group": {"_id": None, "n": {"$sum": "$n_vbs"}}}],
            'facet_vac': [{"$group": {"_id": None, "n": {"$sum": "$vac"}}}],
            'facet_vpm': [{"$project": {"_id": 0, "n_vpm": {"$convert": {"input": "$vpm", "to": "double", "onError": 0, "onNull": 0}}}}, {"$group": {"_id": None, "n": {"$sum": "$n_vpm"}}}],
            'facet_doc': [{"$sortByCount": "$tus"}],
            # 'facet_pmx': [{"$group": {"_id": None, "n": {"$sum": "$pmx"}}}],
        }},
    ])
    return HttpResponse(datos, content_type="application/json")

@login_required(login_url='/login/')
def dash_autorizaciones(request):
    clienteId = '0'
    cliente = 'NUEVO CLIENTE'
    if request.user.cliente:
        clienteId = request.user.cliente.id
        cliente = request.user.cliente.cliente
    return render(request, 'autorizaciones/new_autorizaciones.html', {'clienteId': clienteId, 'cliente': cliente})

def raw_facet_auto(request):
    tema = 'retec_autorizaciones'
    clave = request.POST.get('clave') if request.POST.get('clave') else ''
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    user_id = request.user.id
    consulta = createConsulta('raw_aut_dat' + str(rawper), tema, clave, user_id)
    mongo = Mongo('retec_autorizaciones')
    try:
        datos = mongo.aggregate([
            {'$match': {'crx': periodo} }, 
            {
                '$facet': {
                    'rs_1': [
                        {'$match': {'pmx': {"$in": ['0', 0]}, 'pla': 'S'}}, 
                        {'$group': {'_id': '$nmp', 'valor': {'$sum': '$vbs'}, 'total': {'$sum': 1} }},
                        {'$sort': {'valor': -1}}
                    ], 
                    'rs_2': [
                        {'$match': {'pmx': {"$in": ['0', 0]}, 'pla': 'V'}}, 
                        {'$group': {'_id': '$nmp', 'valor': {'$sum': '$vbs'}, 'total': {'$sum': 1} }},
                        {'$sort': {'valor': -1}}
                    ], 
                    'rs_3': [
                        {'$match': {'pmx': {"$in": ['1', 1]}, 'pla': 'S'}}, 
                        {'$group': {'_id': '$nmp', 'valor': {'$sum': '$vpm'}, 'total': {'$sum': 1} }},
                        {'$sort': {'valor': -1}}
                    ], 
                    'rs_4': [
                        {'$match': {'pmx': {"$in": ['1', 1]}, 'pla': 'V'}}, 
                        {'$group': {'_id': '$nmp', 'valor': {'$sum': '$vpm'}, 'total': {'$sum': 1} }},
                        {'$sort': {'valor': -1}}
                    ],
                    'pmx': [{'$group': {'_id': '$pmx', 'total': {'$sum': 1} } }],
                    'facet_amb': [{"$sortByCount": "$amb"}],
                    'facet_pla': [{"$sortByCount": "$pla"}],
                    'facet_total': [{"$group": {"_id": None, "n": {"$sum": 1}}}],
                    'facet_vbs': [
                        {"$project": {"_id": 0, "n_vbs": {"$convert": {"input": "$vbs", "to": "double", "onError": 0, "onNull": 0}}}}, 
                        {"$group": {"_id": None, "n": {"$sum": "$n_vbs"}}}
                    ],
                    'facet_vac': [{"$group": {"_id": None, "n": {"$sum": "$vac"}}}],
                    'facet_vpm': [
                        {"$project": {"_id": 0, "n_vpm": {"$convert": {"input": "$vpm", "to": "double", "onError": 0, "onNull": 0}}}}, 
                        {"$group": {"_id": None, "n": {"$sum": "$n_vpm"}}}
                    ],
                    'facet_doc': [{"$sortByCount": "$tus"}],
                    'gp_esti': [{'$group': {'_id': '$est', 'total': {'$sum': 1}}}],
                    'gp_stt': [{'$group': {'_id': '$stt', 'total': {'$sum': 1}}}]
                }
            }
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

def raw_facet_auto_control(request):
    tema = 'retec_autorizaciones'
    clave = request.POST.get('clave') if request.POST.get('clave') else ''
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    user_id = request.user.id
    consulta = createConsulta('raw_aut_ctr' + str(rawper), tema, clave, user_id)
    mongo = Mongo(tema)
    try:
        datos = mongo.aggregate([
            {"$match": {'crx': periodo} },
            {"$project": {'factor': {"$multiply": ["$can", "$vun"]}, 'vbs': 1, 'vpm': 1, 'pmx': 1} },
            {"$group": {'_id': '$pmx', 'sum_fac': {"$sum": "$factor"}, 'sum_vbs': {"$sum": "$vbs"}, 'sum_vpm': {"$sum": "$vpm"} } }
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

def schema_auto(request):
    tema = 'retec_autorizaciones'
    clave = request.POST.get('clave') if request.POST.get('clave') else ''
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    user_id = request.user.id
    consulta = createConsulta('schema_auto' + str(rawper), tema, clave, user_id)
    mongo = Mongo(tema)
    try:
        print('iniciando autorization')
        datos = mongo.aggregate([
            {"$match": {'crx': periodo} },
            {'$group': {
                '_id': None,
                'n_stt': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$stt', None] }, None] }, 0, 1] } },
                'n_tpp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tpp', None] }, None] }, 0, 1] } },
                'n_idp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$idp', None] }, None] }, 0, 1] } },
                'n_nmp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$nmp', None] }, None] }, 0, 1] } },
                'n_pla': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$pla', None] }, None] }, 0, 1] } },
                'n_idc': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$idc', None] }, None] }, 0, 1] } },
                'n_tus': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tus', None] }, None] }, 0, 1] } },
                'n_ius': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ius', None] }, None] }, 0, 1] } },
                'n_iav': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$iav', None] }, None] }, 0, 1] } },
                'n_fav': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$fav', None] }, None] }, 0, 1] } },
                'n_amb': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$amb', None] }, None] }, 0, 1] } },
                'n_ids': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ids', None] }, None] }, 0, 1] } },
                'n_ser': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ser', None] }, None] }, 0, 1] } },
                'n_dia': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$dia', None] }, None] }, 0, 1] } },
                'n_can': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$can', None] }, None] }, 0, 1] } },
                'n_est': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$est', None] }, None] }, 0, 1] } },
                'n_vun': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vun', None] }, None] }, 0, 1] } },
                'n_vbs': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vbs', None] }, None] }, 0, 1] } },
                'n_vac': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vac', None] }, None] }, 0, 1] } },
                'n_vpm': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vpm', None] }, None] }, 0, 1] } },
                'n_pmx': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$pmx', None] }, None] }, 0, 1] } },
                'n_pac': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$pac', None] }, None] }, 0, 1] } },
                'n_ume': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ume', None] }, None] }, 0, 1] } },
                'n_ffa': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ffa', None] }, None] }, 0, 1] } },
                'n_cov': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$cov', None] }, None] }, 0, 1] } },
                'total': {'$sum': 1}
            }},
        ])
        consulta.contenido = str(datos)
        consulta.estado = 'close'
        consulta.save()
        return HttpResponse(datos, content_type="application/json")
    except:
        consulta.estado = 'failed'
        consulta.save()
        return HttpResponse([], content_type="application/json")
    
def view_periodo(request):
    return render(request, 'autorizaciones/view_periodo.html')


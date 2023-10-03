from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from morfee_rt_dev.mongo import Mongo
from consulta.views import createConsulta, getConsulta
from datetime import date
import json
# from bson.code import Code

# def createConsulta(name, cole, cla, user):
def pag_panel(request, section):
    if section == 'inicio':
        return pag_inicio(request)
    elif section == 'table':
        return pag_table(request)
    elif section == 'import':
        return pag_import(request)
    elif section == 'dash':
        return pag_dash(request)

def pag_inicio(request):
    return render(request, 'pagos/pag_inicio.html')

def tpl_cuentas_medicas(request):
    return render(request, 'pagos/cuentas_medicas.html')

def pag_table(request):
    coleccion = 'retec_pagos'
    return render(request, 'pagos/pag_table.html', {'coleccion': coleccion})

def pag_import(request):
    coleccion = 'retec_pagos'
    return render(request, 'pagos/pag_import.html', {'coleccion': coleccion})

def data_cm(request):
    clave = request.POST.get('clave') if request.POST.get('clave') else ''
    user_id = request.user.id
    # rawper = int(request.POST.get('periodo'))
    consulta = createConsulta('raw_cmed_pag', 'retec_facturas', clave, user_id)
    mongo = Mongo('retec_pagos')
    print('Exe query mongodb...')
    datos = mongo.aggregate([
        # {"$addFields": {"vraw": {"$toString": "$fr"}} },
        # {"$project": {"vdo": 1, "vgl": 1,  "prd": {"$substrBytes": ["$vraw", 0, 6]}, "vpbs": 1, "vppm": 1, "vpac": 1, "vrpbs": 1, "vrpm": 1, "vrpac": 1} },
        {"$project": {"vdo": 1, "gde": 1, "vr_per": 1, "vpbs": 1, "vppm": 1, "vpac": 1} },
        {"$facet": {
            "result": [
                {"$group": {
                    "_id": "$vr_per", 
                    "v_facturado": {"$sum": "$vdo"}, 
                    "g_definitiva": {"$sum": "$gde"},
                    "pag_pbs": {"$sum": "$vpbs"},
                    "pag_pm": {"$sum": "$vppm"},
                    "pag_pac": {"$sum": "$vpac"},
                }},
                {"$sort": { "_id": 1} },
            ]
        }},
        # {"$limit": 99},
    ])
    print('Print result query...')
    consulta.contenido = str(datos)
    consulta.estado = 'close'
    consulta.save()
    return HttpResponse(datos, content_type="application/json")


def pag_dash(request):
    coleccion = 'retec_pagos'
    mongo = Mongo(coleccion)
    datos = mongo.aggregate([
        {"$facet": {
            'facet_pla': [{"$sortByCount": "$pla"}],
            'facet_amb': [{"$sortByCount": "$amb"}],
            'facet_tra': [{"$sortByCount": "$tra"}],
            'facet_total': [{"$group": {"_id": None, "n": {"$sum": 1}}}],
            'facet_vdo': [{"$group": {"_id": None, "n": {"$sum": "$vdo"}}}],
            'facet_gde': [{"$group": {"_id": None, "n": {"$sum": "$gde"}}}],
            'facet_vpbs': [{"$group": {"_id": None, "n": {"$sum": "$vpbs"}}}],
            'facet_vpac': [{"$group": {"_id": None, "n": {"$sum": "$vpac"}}}],
            'facet_vppm': [{"$group": {"_id": None, "n": {"$sum": "$vppm"}}}],
            'facet_doc': [{"$sortByCount": "$tus"}],
        }},
    ])
    return HttpResponse(datos, content_type="application/json")

def raw_facet_pay(request):
    tema = 'retec_pagos'
    clave = request.POST.get('clave') if request.POST.get('clave') else ''
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    user_id = request.user.id
    consulta = createConsulta('raw_pay_dat' + str(rawper), tema, clave, user_id)
    print('domora + ' + tema)
    mongo = Mongo(tema)
    try:
        datos = mongo.aggregate([
            {'$match': {'crx': periodo}}, 
            {
                '$facet': {
                    # '$vbs'	'$vpm'
                    'rs_0': [ {'$group': {
                        '_id': None, 
                        'total': {'$sum': 1}, 
                        'sum_vdo': {'$sum': "$vdo"}, 
                        'sum_gde': {"$sum": "$gde"}, 
                        'r_pbs': {'$sum': '$vpbs'}, 
                        'r_pm': {'$sum': '$vppm'} 
                    }}],
                    'rs_1': [ {'$group': {'_id': '$pla', 'total': {'$sum': 1}}} ],
                    'rs_2': [ {'$group': {'_id': '$tra', 'total': {'$sum': 1}}} ],
                    'rs_3': [ {'$group': {'_id': '$amb', 'total': {'$sum': 1}}} ],
                    'rs_4': [ {'$group': {'_id': '$tus', 'total': {'$sum': 1}}} ],
                    'pmx':  [ {'$group': {'_id': '$pmx', 'total': {'$sum': 1}}} ],
                    'new_1': [ {'$group': {'_id': '$tpp', 'total': {'$sum': 1}}}],
                    'new_2': [ {'$group': {'_id': '$mpa', 'total': {'$sum': 1}}}],
                    #query  pendiente revizar variables y condiciones.
                    #query para Pagos RS (Ranking)
                    'ran_1a': [
                        {'$match': {'pmx': {"$in": ['0', 0]},  'pla': {'$in': ['S', 'M']}}}, 
                        {'$group': {'_id': '$nmp', 'valor': {'$sum': '$vpbs'}, 'total': {'$sum': 1} }},
                        {'$sort': {'valor': -1}}
                    ], 
                    'ran_1b': [
                        {'$match': {'pmx': {"$in": ['1', 1]}, 'pla': {'$in': ['S', 'M']}}}, 
                        {'$group': {'_id': '$nmp', 'valor': {'$sum': '$vppm'}, 'total': {'$sum': 1} }},
                        {'$sort': {'valor': -1}}
                    ],
                    'ran_2a': [
                        {'$match': {'pmx': {"$in": ['0', 0]}, 'pla':{ '$in':['V', 'C']}}}, 
                        {'$group': {'_id': '$nmp', 'valor': {'$sum': '$vpbs'}, 'total': {'$sum': 1} }},
                        {'$sort': {'valor': -1}}
                    ],                      
                    'ran_2b': [
                        {'$match': {'pmx': {"$in": ['1', 1]}, 'pla':{ '$in':['V', 'C']}}}, 
                        {'$group': {'_id': '$nmp', 'valor': {'$sum': '$vppm'}, 'total': {'$sum': 1} }},
                        {'$sort': {'valor': -1}}
                    ],
                    'ran_3a': [
                        {'$match': {'pmx': {"$in": ['0', 0]}, 'pla':'P'}}, 
                        {'$group': {'_id': '$nmp', 'valor': {'$sum': '$vpac'}, 'total': {'$sum': 1} }},
                        {'$sort': {'valor': -1}}
                    ],
                    'ran_3b': [
                        {'$match': {'pmx': {"$in": ['1', 1]}, 'pla':'P'}}, 
                        {'$group': {'_id': '$nmp', 'valor': {'$sum': '$vpac'}, 'total': {'$sum': 1} }},
                        {'$sort': {'valor': -1}}
                    ], 

                    # 'rs_5': [
                    #     {'$match': {'crx': periodo}}, 
                    #     {'$group': {'_id': {'tm_tra': '$tra', 'tm_tus': '$tus'}, 'total': {'$sum': 1}}}
                    # ]
                }
            }
        ])
        consulta.contenido = str(datos)
        consulta.estado = 'close'
        consulta.save()
        print('dinabot')
        print(datos)
        return HttpResponse(datos, content_type="application/json")
    except:
        consulta.estado = 'failed'
        consulta.save()
        return HttpResponse([], content_type="application/json")

def raw_facet_pay_control(request):
    tema = 'retec_pagos'
    clave = request.POST.get('clave') if request.POST.get('clave') else ''
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    user_id = request.user.id
    consulta = createConsulta('raw_pay_ctr' + str(rawper), tema, clave, user_id)
    mongo = Mongo(tema)
    print('Vanegas Lynch')
    try:
        datos = mongo.aggregate([
            {"$match": {'crx': periodo} },
            {"$addFields": {
                "cd_0": {"$in": ["$pmx", ['0', 0]]},
                "cd_1": {"$in": ["$pmx", ['1', 1]]},
            }},
            {'$group': {
                '_id': None,
                's_vdo': {'$sum': '$vdo'},		# FACTURADO TOTAL
                's_gde': {'$sum': '$gde'},		# GLOSA DEFINITIVA
                's_vpbs': {'$sum': '$vpbs'},	# PAGADO PBS
                's_vppm': {'$sum': '$vppm'},	# PAGADO PM
                'f_pbs': {'$sum': {'$cond': ["$cd_0", '$vdo', 0]}},		# FACTURADO PBS
                'f_pm': {'$sum': {'$cond': ["$cd_1", '$vdo', 0]}},		# FACTURADO PM
                'g_pbs': {'$sum': {'$cond': ["$cd_0", '$gde', 0]}},		# GLOSADO PBS
                'g_pm': {'$sum': {'$cond': ["$cd_1", '$gde', 0]}},		# GLOSADO PM
                'total': {'$sum': 1}
            }}
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

@login_required(login_url='/login/')
def dash_pagos(request):
    clienteId = '0'
    cliente = 'NUEVO CLIENTE'
    if request.user.cliente:
        clienteId = request.user.cliente.id
        cliente = request.user.cliente.cliente
    return render(request, 'pagos/new_pagos.html', {'clienteId': clienteId, 'cliente': cliente})

def schema_pago(request):
    tema = 'retec_pagos'
    clave = request.POST.get('clave') if request.POST.get('clave') else ''
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    user_id = request.user.id
    consulta = createConsulta('schema_pay' + str(rawper), tema, clave, user_id)
    mongo = Mongo(tema)
    try:    
        datos = mongo.aggregate([
            {"$match": {'crx': periodo} },
            {'$group': {
                '_id': None,
                'n_ifa': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ifa', None] }, None] }, 0, 1] } },
                'n_tpp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tpp', None] }, None] }, 0, 1] } },
                'n_idp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$idp', None] }, None] }, 0, 1] } },
                'n_nmp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$nmp', None] }, None] }, 0, 1] } },
                'n_pla': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$pla', None] }, None] }, 0, 1] } },
                'n_tra': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tra', None] }, None] }, 0, 1] } },
                'n_idc': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$idc', None] }, None] }, 0, 1] } },
                'n_tus': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tus', None] }, None] }, 0, 1] } },
                'n_ius': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ius', None] }, None] }, 0, 1] } },
                'n_iau': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$iau', None] }, None] }, 0, 1] } },
                'n_fau': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$fau', None] }, None] }, 0, 1] } },
                'n_amb': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$amb', None] }, None] }, 0, 1] } },
                'n_ids': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ids', None] }, None] }, 0, 1] } },
                'n_ser': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ser', None] }, None] }, 0, 1] } },
                'n_dia': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$dia', None] }, None] }, 0, 1] } },
                'n_can': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$can', None] }, None] }, 0, 1] } },
                'n_fp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$fp', None] }, None] }, 0, 1] } },
                'n_fr': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$fr', None] }, None] }, 0, 1] } },
                'n_vdo': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vdo', None] }, None] }, 0, 1] } },
                'n_gde': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$gde', None] }, None] }, 0, 1] } },
                'n_mpa': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$mpa', None] }, None] }, 0, 1] } },
                'n_vpbs': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vpbs', None] }, None] }, 0, 1] } },
                'n_vpac': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vpac', None] }, None] }, 0, 1] } },
                'n_vppm': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vppm', None] }, None] }, 0, 1] } },
                'n_fpa': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$fpa', None] }, None] }, 0, 1] } },
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
        print(datos)
        return HttpResponse(datos, content_type="application/json")
    except:
        consulta.estado = 'failed'
        consulta.save()
        return HttpResponse([], content_type="application/json")

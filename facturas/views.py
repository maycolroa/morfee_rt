from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from morfee_rt_dev.mongo import Mongo
from consulta.models import Consulta
from datetime import date
import json
# from bson.code import Code

def tpl_cuentas_medicas(request):
    return render(request, 'facturas/cuentas_medicas.html')

def data_cm(request):
    # vdo:VlrFacturado
    # vgl:VlrGlosado
    mongo = Mongo('retec_facturas')
    datos = mongo.aggregate([
        {"$addFields": {"vraw": {"$toString": "$fr"}} },
        {"$project": {"vdo": 1, "vgl": 1,  "prd": {"$substrBytes": ["$vraw", 0, 6]}} }, 
        {"$group": {"_id": "$prd", "v_facturado": {"$sum": "$vdo"}, "v_glosado": {"$sum": "$vgl"}} },
        {"$sort": { "_id": 1} }
    ])
    return HttpResponse(datos, content_type="application/json")

def createConsulta(name, cole, cla, cli, user):
    print('Generando consulta: ' + name)
    try:
        c = Consulta.objects.filter(nombre=name, coleccion=cole, cliente_id=cli, user_id=user).get()
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
        cn.cliente_id = cli
        cn.user_id = user
        cn.save()
        return cn

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

def fac_panel(request, section):
    if section == 'inicio':
        return fac_inicio(request)
    elif section == 'table':
        return fac_table(request)
    elif section == 'import':
        return fac_import(request)
    elif section == 'dash':
        return fac_dash(request)

def fac_inicio(request):
    return render(request, 'facturas/fac_inicio.html')

def fac_table(request):
    coleccion = 'retec_facturas'
    return render(request, 'facturas/fac_table.html', {'coleccion': coleccion})

def fac_import(request):
    coleccion = 'retec_facturas'
    return render(request, 'facturas/fac_import.html', {'coleccion': coleccion})

def fac_dash(request):
    coleccion = 'retec_facturas'
    mongo = Mongo(coleccion)
    datos = mongo.aggregate([
        {"$facet": {
            'facet_amb': [{"$sortByCount": "$amb"}],
            'facet_pla': [{"$sortByCount": "$pla"}],
            'facet_tra': [{"$sortByCount": "$tra"}],
            'facet_total': [{"$group": {"_id": None, "n": {"$sum": 1}}}],
            'facet_vbs': [{"$project": {"_id": 0, "n_vbs": {"$convert": {"input": "$vbs", "to": "double", "onError": 0, "onNull": 0}}}}, {"$group": {"_id": None, "n": {"$sum": "$n_vbs"}}}],
            'facet_vac': [{"$group": {"_id": None, "n": {"$sum": "$vac"}}}],
            'facet_vpm': [{"$project": {"_id": 0, "n_vpm": {"$convert": {"input": "$vpm", "to": "double", "onError": 0, "onNull": 0}}}}, {"$group": {"_id": None, "n": {"$sum": "$n_vpm"}}}],
            'facet_vdo': [{"$project": {"_id": 0, "n_vdo": {"$convert": {"input": "$vdo", "to": "double", "onError": 0, "onNull": 0}}}}, {"$group": {"_id": None, "n": {"$sum": "$n_vdo"}}}],
            'facet_vgl': [{"$project": {"_id": 0, "n_vgl": {"$convert": {"input": "$vgl", "to": "double", "onError": 0, "onNull": 0}}}}, {"$group": {"_id": None, "n": {"$sum": "$n_vgl"}}}],
            'facet_gde': [{"$project": {"_id": 0, "n_gde": {"$convert": {"input": "$gde", "to": "double", "onError": 0, "onNull": 0}}}}, {"$group": {"_id": None, "n": {"$sum": "$n_gde"}}}],
            'facet_doc': [{"$sortByCount": "$tus"}],
        }},
    ])
    return HttpResponse(datos, content_type="application/json")

def raw_facet_fac(request):
    tema = 'retec_facturas'
    clave = request.POST.get('clave') if request.POST.get('clave') else ''
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    cliente_id = request.user.cliente_id if request.user.cliente_id else 0
    user_id = request.user.id
    print(tema)
    print(periodo)
    consulta = createConsulta('raw_facet_fac' + str(rawper), tema, clave, cliente_id, user_id)
    mongo = Mongo(tema)
    print('hola mundo mongo')
    try:
        datos = mongo.aggregate([
            {'$match': {'crx': periodo} }, 
            {
                '$facet': {
                    'rs_0': [ {'$group': {'_id': '$tus', 'total': {'$sum': 1}}} ], 
                    'rs_1': [ {'$group': {'_id': '$pla', 'total': {'$sum': 1}}} ], 
                    'rs_2': [ {'$group': {'_id': '$tra', 'total': {'$sum': 1}}} ], 
                    'rs_3': [ {'$group': {'_id': '$amb', 'total': {'$sum': 1}}} ], 
                    'rs_4': [ {'$group': {'_id': '$egl', 'total': {'$sum': 1}}} ],
                    'pmx':  [ {'$group': {'_id': '$pmx', 'total': {'$sum': 1}}} ],
                    'gp_ext_01': [{'$group': {'_id': '$tpo', 'total': {'$sum': 1}}}], 
                    'gp_ext_02': [{'$group': {'_id': '$tpp', 'total': {'$sum': 1}}}], 
                    'gp_ext_03': [{'$group': {'_id': '$cov', 'total': {'$sum': 1}}}], 
                    'gp_ext_mec': [{'$group': {'_id': '$mpa', 'total': {'$sum': 1}}}],
                    'cores': [
                        {"$project": {
                            "_id": 0, # sum_vpm
                            "n_vac": {"$convert": {"input": "$vac", "to": "double", "onError": 0, "onNull": 0}},
                            "n_vbs": {"$convert": {"input": "$vrpbs", "to": "double", "onError": 0, "onNull": 0}},
                            "n_vpm": {"$convert": {"input": "$vrpm", "to": "double", "onError": 0, "onNull": 0}},
                            "n_vdo": {"$convert": {"input": "$vdo", "to": "double", "onError": 0, "onNull": 0}},
                            "n_vgl": {"$convert": {"input": "$vgl", "to": "double", "onError": 0, "onNull": 0}},
                            "n_gde": {"$convert": {"input": "$gld", "to": "double", "onError": 0, "onNull": 0}} # $gde
                        }}, 
                        {"$group": {
                            "_id": None, 
                            "total": {"$sum": 1},
                            "sum_vac": {"$sum": "$n_vac"},
                            "sum_vbs": {"$sum": "$n_vbs"}, 
                            "sum_vpm": {"$sum": "$n_vpm"}, 
                            "sum_vdo": {"$sum": "$n_vdo"}, 
                            "sum_vgl": {"$sum": "$n_vgl"}, 
                            "sum_gde": {"$sum": "$n_gde"}
                        }},
                    ],
                    's0': [
                        {"$match": {'pmx': {"$in": ['0', 0]}, 'pla': 'S'}},
                        {"$group": {'_id': '$nmp', 'suma': {"$sum": "$vdo"}, 'total': {'$sum': 1}}},
                        {"$sort": {"suma": -1}}
                    ],
                    'v0': [
                        {"$match": {'pmx': {"$in": ['0', 0]}, 'pla': 'V'}},
                        {"$group": {'_id': '$nmp', 'suma': {"$sum": "$vdo"}, 'total': {'$sum': 1}}},
                        {"$sort": {"suma": -1}}
                    ],
                    's1': [
                        {"$match": {'pmx': {"$in": ['1', 1]}, 'pla': 'S'}},
                        {"$group": {'_id': '$nmp', 'suma': {"$sum": "$vdo"}, 'total': {'$sum': 1}}},
                        {"$sort": {"suma": -1}}
                    ],
                    'v1': [
                        {"$match": {'pmx': {"$in": ['1', 1]}, 'pla': 'V'}},
                        {"$group": {'_id': '$nmp', 'suma': {"$sum": "$vdo"}, 'total': {'$sum': 1}}},
                        {"$sort": {"suma": -1}}
                    ],
                }
            }
        ])
        consulta.contenido = str(datos)
        consulta.estado = 'close'
        consulta.save()
        return HttpResponse(datos, content_type="application/json")
    except:
        consulta.estado = 'failed'
        consulta.save()
        return HttpResponse([], content_type="application/json")

def raw_facet_fac_control(request):
    tema = 'retec_facturas'
    clave = request.POST.get('clave') if request.POST.get('clave') else ''
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    cliente_id = request.user.cliente_id if request.user.cliente_id else 0
    user_id = request.user.id
    consulta = createConsulta('raw_fac_ctr' + str(rawper), tema, clave, cliente_id, user_id)
    print('vigo: ' + tema)
    mongo = Mongo(tema)
    try:
        # "n_vbs": {"$convert": {"input": "$vbs", "to": "double", "onError": 0, "onNull": 0}}
        datos = mongo.aggregate([
            {"$match": {'crx': periodo} },
            {"$addFields": {
                "hg": {"$cond": [{"$in": ["$egl", ["T", "P"]]}, 1, 0]}, # hg has_glosa
                "pmx": {"$convert": {"input": "$pmx", "to": "string", "onError": "", "onNull": ""}},
            }},
            {'$project': {
                'vdo': 1,
                'vpbs': 1,
                'vppm': 1,
                'vgl': 1,
                'gld': 1,
                'vrpbs': 1,
                'vrpm': 1,
                'vdo_0_pbs': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$hg", 0]}]}, "$vdo", 0]},
                'vdo_0_pm': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$hg", 0]}]}, "$vdo", 0]},
                'vgl_0_pbs': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$hg", 0]}]}, "$vgl", 0]},
                'vgl_0_pm': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$hg", 0]}]}, "$vgl", 0]},
                'gld_0_pbs': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$hg", 0]}]}, "$gld", 0]},
                'gld_0_pm': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$hg", 0]}]}, "$gld", 0]},
                'vpbs_0': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$hg", 0]}]}, "$vpbs", 0]},
                'vppm_0': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$hg", 0]}]}, "$vppm", 0]},
                'vrpbs_0': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$hg", 0]}]}, "$vrpbs", 0]},
                'vrpm_0': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$hg", 0]}]}, "$vrpm", 0]},
                'vdo_1_pbs': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$egl", "T"]}]}, "$vdo", 0]},
                'vdo_1_pm': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$egl", "T"]}]}, "$vdo", 0]},
                'vgl_1_pbs': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$egl", "T"]}]}, "$vgl", 0]},
                'vgl_1_pm': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$egl", "T"]}]}, "$vgl", 0]},
                'gld_1_pbs': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$egl", "T"]}]}, "$gld", 0]},
                'gld_1_pm': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$egl", "T"]}]}, "$gld", 0]},
                'vpbs_1': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$egl", "T"]}]}, "$vpbs", 0]},
                'vppm_1': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$egl", "T"]}]}, "$vppm", 0]},
                'vrpbs_1': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$egl", "T"]}]}, "$vrpbs", 0]},
                'vrpm_1': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$egl", "T"]}]}, "$vrpm", 0]},
                'vdo_2_pbs': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$egl", "P"]}]}, "$vdo", 0]},
                'vdo_2_pm': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$egl", "P"]}]}, "$vdo", 0]},
                'vgl_2_pbs': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$egl", "P"]}]}, "$vgl", 0]},
                'vgl_2_pm': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$egl", "P"]}]}, "$vgl", 0]},
                'gld_2_pbs': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$egl", "P"]}]}, "$gld", 0]},
                'gld_2_pm': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$egl", "P"]}]}, "$gld", 0]},
                'vpbs_2': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$egl", "P"]}]}, "$vpbs", 0]},
                'vppm_2': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$egl", "P"]}]}, "$vppm", 0]},
                'vrpbs_2': {"$cond": [{"$and": [{"$eq": ["$pmx", "0"]}, {"$eq": ["$egl", "P"]}]}, "$vrpbs", 0]},
                'vrpm_2': {"$cond": [{"$and": [{"$eq": ["$pmx", "1"]}, {"$eq": ["$egl", "P"]}]}, "$vrpm", 0]},
            }},
            {'$group': {
                '_id': None,
                's_vdo': {'$sum': '$vdo'},
                's_vpbs': {'$sum': '$vpbs'},
                's_vppm': {'$sum': '$vppm'},
                's_vgl': {'$sum': '$vgl'},
                's_gld': {'$sum': '$gld'},
                's_vrpbs': {'$sum': '$vrpbs'},
                's_vrpm': {'$sum': '$vrpm'},
                's_vdo_0_pbs': {'$sum': '$vdo_0_pbs'},
                's_vdo_0_pm': {'$sum': '$vdo_0_pm'},
                's_vgl_0_pbs': {'$sum': '$vgl_0_pbs'},
                's_vgl_0_pm': {'$sum': '$vgl_0_pm'},
                's_gld_0_pbs': {'$sum': '$gld_0_pbs'},
                's_gld_0_pm': {'$sum': '$gld_0_pm'},
                's_vpbs_0': {'$sum': '$vpbs_0'},
                's_vppm_0': {'$sum': '$vppm_0'},
                's_vrpbs_0': {'$sum': '$vrpbs_0'},
                's_vrpm_0': {'$sum': '$vrpm_0'},
                's_vdo_1_pbs': {'$sum': '$vdo_1_pbs'},
                's_vdo_1_pm': {'$sum': '$vdo_1_pm'},
                's_vgl_1_pbs': {'$sum': '$vgl_1_pbs'},
                's_vgl_1_pm': {'$sum': '$vgl_1_pm'},
                's_gld_1_pbs': {'$sum': '$gld_1_pbs'},
                's_gld_1_pm': {'$sum': '$gld_1_pm'},
                's_vpbs_1': {'$sum': '$vpbs_1'},
                's_vppm_1': {'$sum': '$vppm_1'},
                's_vrpbs_1': {'$sum': '$vrpbs_1'},
                's_vrpm_1': {'$sum': '$vrpm_1'},
                's_vdo_2_pbs': {'$sum': '$vdo_2_pbs'},
                's_vdo_2_pm': {'$sum': '$vdo_2_pm'},
                's_vgl_2_pbs': {'$sum': '$vgl_2_pbs'},
                's_vgl_2_pm': {'$sum': '$vgl_2_pm'},
                's_gld_2_pbs': {'$sum': '$gld_2_pbs'},
                's_gld_2_pm': {'$sum': '$gld_2_pm'},
                's_vpbs_2': {'$sum': '$vpbs_2'},
                's_vppm_2': {'$sum': '$vppm_2'},
                's_vrpbs_2': {'$sum': '$vrpbs_2'},
                's_vrpm_2': {'$sum': '$vrpm_2'},
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

def raw_facet_fac_indi(request):
    tema = 'retec_facturas'
    mongo = Mongo(tema)
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    datos = mongo.aggregate([
        {"$match": {'crx': periodo} },
        {'$group': {
            '_id': None,
            's_vdo': {'$sum': '$vrpbs'},
            's_vpbs': {'$sum': '$vrpm'},
            'total': {'$sum': 1}
        }}
    ])
    return HttpResponse(datos, content_type="application/json")

@login_required(login_url='/login/')
def dash_facturas(request):
    clienteId = '0'
    cliente = 'NUEVO CLIENTE'
    indigena = 'off'
    if request.user.cliente:
        clienteId = request.user.cliente.id
        cliente = request.user.cliente.cliente
        if request.user.cliente.is_indigena:
            indigena = 'on'
    return render(request, 'facturas/new_facturas.html', {'clienteId': clienteId, 'cliente': cliente, 'indigena': indigena})

def schema_factura(request):
    # fields="tpo:tipoObligacion|ifa:idFactura|tpp:tipoIdPrestador|idp:idPrestador|nmp:nombrePrestador|pla:planSalud|tra:TContra|idc:idContrato|tus:tipoIdUsuario|ius:idUsuario|iav:idAvisado|fau:FAuto|amb:Ambito|ids:idServicio|ser:DesServicio|dia:DiagPpal|can:Cant|fp:FPres|fr:FRad|vdo:VlrFacturado|vpbs:VlrPagadoPBS|vpac:VlrPagadoPAC|vppm:VlrPagadoPM|fpa:FPago|mpa:MecPago|egl:EstGlosa|vgl:VlrGlosado|gld:glosaDefinitiva|vrpbs:VlrReservaPBS|vrpac:VlrReservaPAC|vrpm:VlrReservaPM|pmx:pres_Max|pac:PAct|ume:UMed|ffa:FFarma|cov:Covid"
    tema = 'retec_facturas'
    clave = request.POST.get('clave') if request.POST.get('clave') else ''
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    cliente_id = request.user.cliente_id if request.user.cliente_id else 0
    user_id = request.user.id
    consulta = createConsulta('schema_factura' + str(rawper), tema, clave, cliente_id, user_id)
    mongo = Mongo(tema)
    try:
        datos = mongo.aggregate([
            {"$match": {'crx': periodo} },
            {'$group': {
                '_id': None,
                               #  {$cond: [{$eq: [{$ifNull: ["$vpac", null] }, null] }, 0, 1] } },
                'n_tpo': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tpo', None] }, None] }, 0, 1] } },
                'n_ifa': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ifa', None] }, None] }, 0, 1] } },
                'n_tpp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tpp', None] }, None] }, 0, 1] } },
                'n_idp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$idp', None] }, None] }, 0, 1] } },
                'n_nmp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$nmp', None] }, None] }, 0, 1] } },
                'n_pla': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$pla', None] }, None] }, 0, 1] } },
                'n_tra': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tra', None] }, None] }, 0, 1] } },
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
                'n_fp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$fp', None] }, None] }, 0, 1] } },
                'n_fr': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$fr', None] }, None] }, 0, 1] } },
                'n_vdo': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vdo', None] }, None] }, 0, 1] } },
                'n_vpbs': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vpbs', None] }, None] }, 0, 1] } },
                'n_vpac': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vpac', None] }, None] }, 0, 1] } },
                'n_vppm': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vppm', None] }, None] }, 0, 1] } },
                'n_fpa': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$fpa', None] }, None] }, 0, 1] } },
                'n_mpa': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$mpa', None] }, None] }, 0, 1] } },
                'n_egl': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$egl', None] }, None] }, 0, 1] } },
                'n_vgl': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vgl', None] }, None] }, 0, 1] } },
                'n_gld': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$gld', None] }, None] }, 0, 1] } },
                'n_vrpbs': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vrpbs', None] }, None] }, 0, 1] } },
                'n_vrpac': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vrpac', None] }, None] }, 0, 1] } },
                'n_vrpm': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$vrpm', None] }, None] }, 0, 1] } },
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

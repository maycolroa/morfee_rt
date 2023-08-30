from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from morfee_rt_dev.mongo import Mongo
from consulta.models import Consulta
from datetime import date
import json
# from bson.code import Code

def createConsulta(name, cole, cla, cli, user):
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

def cont_panel(request, section):
    if section == 'inicio':
        return cont_inicio(request)
    elif section == 'table':
        return cont_table(request)
    elif section == 'import':
        return cont_import(request)
    elif section == 'dash':
        return cont_dash(request)
    elif section == 'extra':
        return cont_extra(request)

def cont_inicio(request):
    coleccion = 'retec_contratos'
    return render(request, 'contratos/cont_inicio.html', {'coleccion': coleccion})

def cont_import(request):
    coleccion = 'retec_contratos'
    return render(request, 'contratos/cont_import.html', {'coleccion': coleccion})

def cont_table(request):
    coleccion = 'retec_contratos'
    return render(request, 'contratos/cont_table.html', {'coleccion': coleccion})

def cont_dash(request):
    coleccion = 'retec_contratos'
    mongo = Mongo(coleccion)
    datos = mongo.aggregate([
        {"$facet": {
            'facet_pla': [{"$sortByCount": "$pla"}],
            'facet_base': [{"$group": {"_id": "", "base": {"$sum": "$bas"}}}],
            'facet_actual': [{"$group": {"_id": "", "actual": {"$sum": "$act"}}}],
            'facet_total': [{"$group": {"_id": None, "n": {"$sum": 1}}}],
            'facet_pre': [{"$group": {"_id": "$idp"}}],
            'facet_doc': [{"$sortByCount": "$tpp"}],
            # 'facet_suma': [{"$project": {"base": {"$sum": "$bas"}, "actual": {"$sum": "$act"}}}],
            # {"$group": {"_id": "$depmun", "total": {"$sum": 1}}}
        }},
    ])
    return HttpResponse(datos, content_type="application/json")

def cont_extra(request):
    coleccion = 'retec_contratos'
    mongo = Mongo(coleccion)
    datos = mongo.getCliente().count()
    mongo.close()
    return HttpResponse(datos, content_type="application/json")

def raw_facet(request):
    tema = 'retec_contratos'
    clave = request.POST.get('clave') if request.POST.get('clave') else ''
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    cliente_id = request.user.cliente_id if request.user.cliente_id else 0
    user_id = request.user.id
    consulta = createConsulta('raw_ctro_dat' + str(rawper), tema, clave, cliente_id, user_id)
    mongo = Mongo(tema)
    try:
        # 'facet_base': [{"$group": {"_id": "", "base": {"$sum": "$bas"}}}],
        # 'facet_actual': [{"$group": {"_id": "", "actual": {"$sum": "$act"}}}],
        datos = mongo.aggregate([
            {'$match': {'crx': periodo}}, 
            {
                '$facet': {
                    'rs_1': [ {'$group': {'_id': '$pla', 'total': {'$sum': 1}, 'suma': {'$sum': '$act'}}} ], 
                    'rs_2': [ {'$group': {'_id': '$tpp', 'total': {'$sum': 1}, 'suma': {'$sum': '$act'}}} ], 
                    'rs_3': [ {'$group': {'_id': '$stt', 'total': {'$sum': 1}, 'suma': {'$sum': '$act'}}} ], 
                    'rs_4': [ {'$group': {'_id': None, 'suma': {'$sum': '$bas'}}} ], 
                    'rs_5': [ {'$group': {'_id': None, 'suma': {'$sum': '$act'}, 'alldoc': {'$sum': 1} }} ], 
                    'rs_6': [
                        {'$group': {'_id': '$nmp', 'total': {'$sum': 1}, 'suma': {'$sum': '$act'}}}, 
                        {'$sort': {'suma': -1}}, 
                        {'$limit': 20}
                    ],
                    'rs_7': [ {'$group': {'_id': '$idp', 'total': {'$sum': 1}}} ],
                    'rs_8': [
                        {'$addFields': {'xnum': {"$convert": {"input": "$tar", "to": "string", "onError": "error", "onNull": "null"}} }},
                        {'$group': {'_id': '$xnum', 'total': {'$sum': 1}}} 
                    ]
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

@login_required(login_url='/login/')
def dash_contratos(request):
    clienteId = '0'
    cliente = 'NUEVO CLIENTE'
    if request.user.cliente:
        clienteId = request.user.cliente.id
        cliente = request.user.cliente.cliente
    return render(request, 'contratos/new_contratos.html', {'clienteId': clienteId, 'cliente': cliente})

def schema_contrato(request):
    tema = 'retec_contratos'
    clave = request.POST.get('clave') if request.POST.get('clave') else ''
    rawper = int(request.POST.get('periodo'))
    periodo = {"$exists": False} if rawper == 0 else rawper
    cliente_id = request.user.cliente_id if request.user.cliente_id else 0
    user_id = request.user.id
    consulta = createConsulta('schema_ctro' + str(rawper), tema, clave, cliente_id, user_id)
    mongo = Mongo(tema)
    try:    
        datos = mongo.aggregate([
            {"$match": {'crx': periodo} },
            {'$group': {
                '_id': None,
                'n_tpp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tpp', None] }, None] }, 0, 1] } },
                'n_idp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$idp', None] }, None] }, 0, 1] } },
                'n_nmp': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$nmp', None] }, None] }, 0, 1] } },
                'n_pla': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$pla', None] }, None] }, 0, 1] } },
                'n_idc': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$idc', None] }, None] }, 0, 1] } },
                'n_stt': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$stt', None] }, None] }, 0, 1] } },
                'n_f1': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$f1', None] }, None] }, 0, 1] } },
                'n_f2': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$f2', None] }, None] }, 0, 1] } },
                'n_ids': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ids', None] }, None] }, 0, 1] } },
                'n_ser': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$ser', None] }, None] }, 0, 1] } },
                'n_tar': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$tar', None] }, None] }, 0, 1] } },
                'n_bas': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$bas', None] }, None] }, 0, 1] } },
                'n_act': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$act', None] }, None] }, 0, 1] } },
                'n_f3': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$f3', None] }, None] }, 0, 1] } },
                'n_f4': {'$sum': {'$cond': [{'$eq': [{'$ifNull': ['$f4', None] }, None] }, 0, 1] } },
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

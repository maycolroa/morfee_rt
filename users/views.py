from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from . import forms, models
from morfee_rt_dev.mongo import Mongo
from time import sleep
import json, datetime
import pandas as pd

# Create your views here.
def tpl_prueba(request):
    sleep(5)
    return render(request, 'users/prueba.html')

def date_to_string(fl):
    if isinstance(fl, datetime.date):
        return fl.isoformat()

def import_history(request):
    if request.method == 'POST':
        colec = request.POST.get('coleccion')
        print(colec)
        datos = models.ControlImportBasic.objects.filter(coleccion=colec).values('id', 'coleccion', 'created_at', 'total')
        lista = list(datos)
        rs = json.dumps(lista, default=date_to_string)
        return HttpResponse(rs, content_type="application/json")
    else:
        return JsonResponse([], content_type="application/json")
    
# SECTION USERS
@login_required(login_url='/login/')
def user_list(request):
   datos = models.UserMorfee.objects.all()
   return render(request, 'users/user_list.html', {'datos': datos})

@login_required(login_url='/login/')
def user_preselect(request):
    return render(request, 'users/user_preselect.html')

@login_required(login_url='/login/')
def user_add(request):
    if request.method == "POST":
        form = forms.UserMorfeeForm(request.POST)
        if form.is_valid():
            user = models.UserMorfee()
            user.username = request.POST.get('username')
            user.set_password(request.POST.get('password1'))
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
           # user.cliente = models.AuthCliente.objects.get(pk=request.POST.get('cliente'))
            user.rol = models.AuthRol.objects.get(pk=request.POST.get('rol'))
            user.save()
            return redirect('ad_user_list')
        else:
            return render(request, 'users/user_add.html', {'form': form})
    else:
        return render(request, 'users/user_add.html', {'form': forms.UserMorfeeForm()})

@login_required(login_url='/login/')
def user_add_staff(request):
    if request.method == "POST":
        form = forms.UserStaffForm(request.POST)
        if form.is_valid():
            user = models.UserMorfee()
            user.username = request.POST.get('username')
            user.set_password(request.POST.get('password1'))
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.is_staff = True
            user.save()
            return redirect('ad_user_list')
        else:
            return render(request, 'users/user_add_staff.html', {'form': form})
    else:
        return render(request, 'users/user_add_staff.html', {'form': forms.UserStaffForm()})

@login_required(login_url='/login/')
def user_edit(request, id):
    try:
        user = models.UserMorfee.objects.get(pk=id)
        plantilla = 'users/user_edit_staff.html' if user.is_superuser or user.is_staff else 'users/user_edit.html'
        if request.method == "POST":
            form = forms.UserEditStaffForm(request.POST, instance=user) if user.is_superuser or user.is_staff else forms.UserEditForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('ad_user_list')
            else:
                return render(request, plantilla, {'form': form, 'usuario': user})
        else:
            form = forms.UserEditStaffForm(instance=user) if user.is_superuser or user.is_staff else forms.UserEditForm(instance=user)
            return render(request, plantilla, {'form': form, 'usuario': user})
    except models.UserMorfee.DoesNotExist:
        return render(request, 'users/not_found.html', {'mensaje': 'No se pudo encontrar el registro solicitado, por favor consulte con el administrador del sitio.'})

@login_required(login_url='/login/')
def user_remove(request, id):
    try:
        user = models.UserMorfee.objects.get(pk=id)
        if not user.is_superuser:
            try:
                user.delete()
                return redirect('ad_user_list')
            except models.UserMorfee.DoesNotExist:
                return render(request, 'morfeeweb/not_found.html', {'titulo': 'Mi titulo', 'mensaje': 'No se pudo encontrar el registro solicitado, por lo tanto, no se puede eliminar, por favor consulte con el administrador del sitio.'})
        else:
            return redirect('ad_user_list')
    except models.UserMorfee.DoesNotExist:
        return render(request, 'users/not_found.html', {'mensaje': 'No se pudo encontrar el registro solicitado, por favor consulte con el administrador del sitio.'})

def user_edit(request, id):
    try:
        user = models.UserMorfee.objects.get(pk=id)
        plantilla = 'users/user_edit_staff.html' if user.is_superuser or user.is_staff else 'users/user_edit.html'
        if request.method == "POST":
            form = forms.UserEditStaffForm(request.POST, instance=user) if user.is_superuser or user.is_staff else forms.UserEditForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('ad_user_list')
            else:
                return render(request, plantilla, {'form': form, 'usuario': user})
        else:
            form = forms.UserEditStaffForm(instance=user) if user.is_superuser or user.is_staff else forms.UserEditForm(instance=user)
            return render(request, plantilla, {'form': form, 'usuario': user})
    except models.UserMorfee.DoesNotExist:
        return render(request, 'users/not_found.html', {'mensaje': 'No se pudo encontrar el registro solicitado, por favor consulte con el administrador del sitio.'})

def import_delete_basic(request):
    if request.method == "POST":
        id = request.POST.get('codex')
        coleccion = request.POST.get('coleccion')
        try:
            target = models.ControlImportBasic.objects.get(pk=id)
            if target.coleccion == coleccion:
                mongo = Mongo(coleccion)
                if mongo.removeImport(target.id):
                    target.delete()
                    return JsonResponse({'status': 'success'})
                else:
                    return JsonResponse({'status': 'failed', 'msn': 'Falló la eliminación en MongoDB'})
            else:
                return JsonResponse({'status': 'failed', 'msn': 'Las credenciales fallaron'})
        except models.ControlImportBasic.DoesNotExist:
            return JsonResponse({'status': 'failed', 'msn': 'No se encontró la importación referenciada. CTR-' + str(id)})

def getImport(request):
    codigo = request.POST.get('codigo')
    mnu = None
    try:
        imp = models.ControlImportBasic.objects.get(clave=codigo)
        mnu = {'id': imp.id, 'total': imp.total, 'clave': imp.clave, 'estado': imp.estado}
    except models.ControlImportBasic.DoesNotExist:
        mnu = {'id': '', 'total': 0, 'clave': codigo, 'estado': 'void'}
    return JsonResponse(mnu)

def basic_import_add(request):
    print('Into basic_import_add')
    periodo = request.POST.get('periodo')
    coleccion = request.POST.get('coleccion')
    print('Coleccion: ' + coleccion)
    type_head = request.POST.get('type_head')
    print('Type_head: ' + type_head)
    delimit = request.POST.get('delimitador')
    print('Delimit: ' + delimit)
    campos = request.POST.get('campos')
    print('Campos: ' + campos)
    codigo = '' if request.POST.get('codigo') == None else request.POST.get('codigo')
    print('Código: ' + codigo)
    campos_list = campos.split('|')
    print('Lista de campos ▼')
    print(campos_list)
    reglas = request.POST.get('reglas')
    print('Reglas: ' + reglas)
    mycodec = request.POST.get('codec')
    print('Codec: ' + mycodec)
    merror = 'strict' if request.POST.get('merror') == None else request.POST.get('merror')
    print('Merror: ' + merror)
    reglas_dict = None if reglas == '' else {x.split(':')[0]: x.split(':')[1] for x in reglas.split('|')}
    imp = models.ControlImportBasic()
    imp.coleccion = coleccion
    imp.campos = '' # campos
    imp.cliente = request.user.cliente
    imp.user = request.user
    imp.clave = codigo
    imp.estado = 'ini'
    imp.save()
    print('Rastreo: ' + str(imp.id))
    mongo = Mongo(coleccion)
    content = None
    result = 0
    campos_str = ''
    rawFile = request.FILES.get("rawfile")
    mensaje = 'none'
    # codecs = ['ascii','big5','big5hkscs','cp037','cp273','cp424','cp437','cp500','cp720','cp737','cp775','cp850','cp852','cp855','cp856','cp857','cp858','cp860','cp861','cp862','cp863','cp864','cp865','cp866','cp869','cp874','cp875','cp932','cp949','cp950','cp1006','cp1026','cp1125','cp1140','cp1250','cp1251','cp1252','cp1253','cp1254','cp1255','cp1256','cp1257','cp1258','euc_jp','euc_jis_2004','euc_jisx0213','euc_kr','gb2312','gbk','gb18030','hz','iso2022_jp','iso2022_jp_1','iso2022_jp_2','iso2022_jp_2004','iso2022_jp_3','iso2022_jp_ext','iso2022_kr','latin_1','iso8859_2','iso8859_3','iso8859_4','iso8859_5','iso8859_6','iso8859_7','iso8859_8','iso8859_9','iso8859_10','iso8859_11','iso8859_13','iso8859_14','iso8859_15','iso8859_16','johab','koi8_r','koi8_t','koi8_u','kz1048','mac_cyrillic','mac_greek','mac_iceland','mac_latin2','mac_roman','mac_turkish','ptcp154','shift_jis','shift_jis_2004','shift_jisx0213','utf_32','utf_32_be','utf_32_le','utf_16','utf_16_be','utf_16_le','utf_7','utf-8','utf_8_sig']
    # codec = 'utf-8'
    # After dtype param push codec
    # encoding=codec, 
    mnu = 0
    try:
        if type_head == 'auto':
            # content = pd.read_csv(rawFile, delimiter=delimit, header=None, names=campos_list, dtype=reglas_dict, encoding=codec, keep_default_na=False)
            # Las cabeceras no se incluyen en el archivo, deben ser suministradas por campos_list
            with pd.read_csv(rawFile, delimiter=delimit, header=None, names=campos_list, dtype=reglas_dict, encoding=mycodec, encoding_errors=merror, keep_default_na=False, chunksize=40000, low_memory=False) as reader:
                for chunk in reader:
                    if periodo:
                        chunk['crx'] = int(periodo)
                    chunk['ctr'] = imp.id
                    docs = chunk.to_dict(orient='records')
                    result += mongo.insertManyChunk(docs)
                mongo.close()
        elif type_head == 'file_parse':
            # Las cabeceras se incluyen en el archivo, pero se salta la primera línea.
            with pd.read_csv(rawFile, delimiter=delimit, header=None, names=campos_list, dtype=reglas_dict, encoding=mycodec, encoding_errors=merror, keep_default_na=False, chunksize=1000, low_memory=False, skiprows=1) as reader:
                print('Abrió el archivo...')
                print('Chunksize: 1000')
                imp.estado = 'open'
                imp.save()
                for chunk in reader:
                    if periodo:
                        chunk['crx'] = int(periodo)
                    chunk['ctr'] = imp.id
                    docs = chunk.to_dict(orient='records')
                    parcial = mongo.insertManyChunk(docs)
                    result += parcial
                    mnu += 1
                    if mnu % 10 == 0:
                        imp.total = result
                        imp.save()
                    print(f'Chunk: {mnu}, len: {parcial}')
                mongo.close()
        else:   # file_fixed
            # Se salta la primera línea
            with pd.read_csv(rawFile, delimiter=delimit, header=None, names=campos_list, dtype=reglas_dict, encoding=mycodec, encoding_errors=merror, keep_default_na=False, chunksize=40000, low_memory=False, skiprows=1) as reader:
                for chunk in reader:
                    if periodo:
                        chunk['crx'] = int(periodo)
                    chunk['ctr'] = imp.id
                    docs = chunk.to_dict(orient='records')
                    result += mongo.insertManyChunk(docs)
                mongo.close()
            # campos_in_line = content.columns.values.tolist()
            # campos_str = "|".join(campos_in_line)
            # Here block analisys headers type_head
            imp.campos = campos_str
        mensaje = 'success'
    except Exception as e:
        mensaje = str(e)
    
    if mensaje == 'success':
        if result > 0:
            imp.total = result
            imp.estado = 'close'
            imp.save()
            return JsonResponse({'status': 'success', 'total': result})
        else:
            imp.delete()
            return JsonResponse({'status': 'failed', 'total': result, 'msn': 'Failed insert many in mongodb.'})
    else:
        imp.estado = 'close'
        imp.save()
        return JsonResponse({'status': 'failed', 'total': result, 'msn': mensaje})

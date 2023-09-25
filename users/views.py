from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from . import forms, models
from time import sleep
import json, datetime
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



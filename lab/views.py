from django.shortcuts import render

def tpl_santiago(request):
    return render(request, 'lab/santiago.html')

def tpl_xml(request):
    return render(request, 'lab/lector.html')

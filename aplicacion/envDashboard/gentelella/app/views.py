from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from functions.clasificador import correrClasificador
from functions.evaluacionModelo import entrenarClasificador
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def index(request):
    context = {}
    template = loader.get_template('app/clasificador.html')
    return HttpResponse(template.render(context, request))


def gentella_html(request):
    context = {}
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))

@csrf_exempt
def ajax_parametros_clasificador(request):
    #if request.is_ajax() and request.method == 'GET':
    if request.method == 'POST':
        fechaInicio = request.POST['fechaInicio']
        fechaFin = request.POST['fechaFin']
        data = correrClasificador(fechaInicio, fechaFin)

         # try:
         #    fechaInicio = request.GET['fechaInicio']
         #    fechaFin = request.GET['fechaFin']
         #    data = correrClasificador(fechaInicio, fechaFin)
         #    if not data:
         #        data = {'status': 'error', 'mensaje': 'No se pudo correr el clasificador, favor revisar las fechas seleccionadas'}
         # except:
         #    data = {'status' : 'error', 'mensaje' : 'No se pudo correr el clasificador'}

    else:
        data = {'status': 'error', 'mensaje': 'La peticion no es ajax o no es tipo POST'}
    return JsonResponse(data)

def handle_uploaded_file(f):
    with open('app/functions/datos/nuevoEntrenamiento.csv', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@csrf_exempt
def ajax_upload_file(request):
    if request.method == 'POST':
        handle_uploaded_file(request.FILES['file'])
    data = {'status': 'ok', 'mensaje': 'Se cargo con exito'}
    return JsonResponse(data)

@csrf_exempt
def ajax_correr_entrenamiento(request):
    if request.is_ajax() and request.method == 'POST':
        try:
            data = entrenarClasificador()
            if not data:
                data = {'status': 'error', 'mensaje': 'No se pudo realizar el entrenamiento'}
        except:
           data = {'status' : 'error', 'mensaje' : 'Ocurrio un error tratando de realizar el entrenamiento'}
    else:
        data = {'status': 'error', 'mensaje': 'La peticion no es ajax o no es tipo POST'}

    return JsonResponse(data)

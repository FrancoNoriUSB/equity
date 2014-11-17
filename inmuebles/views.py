from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from datetime import datetime, date
from django.forms.models import inlineformset_factory
from django.db.models import Count
from django.db.models import Q
from inmuebles.models import *
from inmuebles.forms import *
from noticias.models import *
from functions import *
from django.core.mail.message import EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_countries import countries


# Vista del index o home
def index(request):

    ctx = {
    
    }

    return render_to_response('index/index.html', ctx, context_instance=RequestContext(request))

def home(request, pais):

    #Busqueda del nombre del pais a partir del codigo
    for code, name in list(countries):
        if code == pais:
            pais = name
            code = code
            break

    #Formulario para los paises disponibles
    paisesF = PaisesForm(initial={'pais':pais,})

    if request.POST:
        paisesF = PaisesForm(request.POST)
        if paisesF.is_valid():

            pais = paisesF.cleaned_data['pais']
            for code, name in list(countries):
                if name == pais:
                    pais = code
                    break

            pais = Pais.objects.get(nombre=pais)
            return HttpResponseRedirect('/'+str(pais.nombre)+'/')

    #Busqueda de propiedades en el pais actual
    pais = code
    inmuebles_list = Inmueble.objects.filter(pais__nombre=pais)
    paginator = Paginator(inmuebles_list, 6)
    page = request.GET.get('page')

    try:
        inmuebles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        inmuebles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        inmuebles = paginator.page(paginator.num_pages)

    ctx = {
        'paisesF':paisesF,
        'pais':pais,
        'inmuebles': inmuebles,
    }

    return render_to_response('home/home.html', ctx, context_instance=RequestContext(request))

def inmueble(request, codigo, pais):

    #Formulario para los paises disponibles
    paisesF = PaisesForm(request.POST)

    ctx = {
        'paisesF':paisesF,
        'pais':pais,
    }

    return render_to_response('inmueble/inmueble.html', ctx, context_instance=RequestContext(request))
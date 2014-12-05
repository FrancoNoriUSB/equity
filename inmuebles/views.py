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

    #Formulario para los paises disponibles
    paisesF = PaisesForm()

    ctx = {
        'PaisesForm':paisesF,
    }

    return render_to_response('index/index.html', ctx, context_instance=RequestContext(request))


#Vista del home de cada pais
def home(request, pais):

    #Buscador de inmuebles
    buscadorF = BuscadorForm()
    buscadorF.fields['ciudad'] = forms.ModelChoiceField(Ciudad.objects.filter(pais__nombre=pais), empty_label=' - Ciudad -')
    buscadorF.fields['zona'] = forms.ModelChoiceField(Zona.objects.filter(ciudad__pais__nombre=pais), empty_label=' - Zona -')

    #Formulario para los paises disponibles
    paisesF = PaisesForm(initial={
        'pais':pais,
    })

    #Busqueda de propiedades en el pais actual
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
        'buscadorF':buscadorF,
        'paisesF':paisesF,
        'pais':pais,
        'inmuebles': inmuebles,
    }

    return render_to_response('home/home.html', ctx, context_instance=RequestContext(request))


#Vista de cada inmueble
def inmueble(request, codigo, pais):

    #Buscador de inmuebles
    buscadorF = BuscadorForm()
    buscadorF.fields['ciudad'] = forms.ModelChoiceField(Ciudad.objects.filter(pais__nombre=pais), empty_label=' - Ciudad -')
    buscadorF.fields['zona'] = forms.ModelChoiceField(Zona.objects.filter(ciudad__pais__nombre=pais), empty_label=' - Zona -')

    #Formulario para los paises disponibles
    paisesF = PaisesForm(initial={
        'pais':pais,
    })

    ctx = {
        'buscadorF':buscadorF,
        'paisesF':paisesF,
        'pais':pais,
    }

    return render_to_response('inmueble/inmueble.html', ctx, context_instance=RequestContext(request))
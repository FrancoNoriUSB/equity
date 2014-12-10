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
from django.views.generic import TemplateView, CreateView
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
from django import forms


# Vista del index o home
def index(request):

    #Formulario para los paises disponibles
    paisesF = PaisesForm()

    ctx = {
        'PaisesForm': paisesF,
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
        'pais': pais,
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
        'buscadorF': buscadorF,
        'paisesF': paisesF,
        'pais': pais,
        'inmuebles': inmuebles,
    }

    return render_to_response('home/home.html', ctx, context_instance=RequestContext(request))


#Vista de cada inmueble
def inmueble(request, codigo, pais):

    #Buscador de inmuebles
    buscadorF = BuscadorForm()
    buscadorF.fields['ciudad'] = forms.ModelChoiceField(Ciudad.objects.filter(pais__nombre=pais), empty_label=' - Ciudad -')
    buscadorF.fields['zona'] = forms.ModelChoiceField(Zona.objects.filter(ciudad__pais__nombre=pais), empty_label=' - Zona -')

    #Contacto con el agente
    contactoF = ContactoAgenteForm()

    #Formulario para los paises disponibles
    paisesF = PaisesForm(initial={
        'pais': pais,
    })

    ctx = {
        'buscadorF': buscadorF,
        'ContactoAgenteForm': contactoF,
        'paisesF': paisesF,
        'pais': pais,
    }

    return render_to_response('inmuebles/inmueble.html', ctx, context_instance=RequestContext(request))


# Vista para elegir el tipo de inmueble a publicar
class ElegirTipo(TemplateView):

    template_name = "inmuebles/elegir-tipo.html"

    def get_context_data(self, **kwargs):
        context = super(ElegirTipo, self).get_context_data(**kwargs)
        context['pais'] = kwargs["pais"]
        return context


#Vista para publicar el inmueble
class Publicar(CreateView):
    template_name = 'inmuebles/publicar.html'
    model = Inmueble
    form = InmuebleForm
    fields = ['titulo', 'codigo', 'descripcion', 'ciudad', 'zona', 'direccion', 'agente', 'latitud', 'longitud']

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        tipo = get_object_or_404(TipoInmueble, nombre=kwargs["tipo"])
        campos = CampoTipoInmueble.objects.filter(tipo_inmueble=tipo)
        ValorCampoTipoInmuebleFormset = inlineformset_factory(Inmueble,
                                                              ValorCampoTipoInmueble,
                                                              extra=campos.count(),
                                                              can_delete=False,
                                                              fields=['campo', 'valor'])
        campotipo_formset = ValorCampoTipoInmuebleFormset()
        for formset in campotipo_formset:
            formset.fields['campo'].choices = campos.values_list('id', 'nombre')
        imagen_formset = ImagenFormset()
        campo_formset = CampoFormset()
        return self.render_to_response(self.get_context_data(form=form,
                                                             campotipo_formset=campotipo_formset,
                                                             imagen_formset=imagen_formset,
                                                             campo_formset=campo_formset,
                                                             pais=kwargs["pais"]))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        tipo = get_object_or_404(TipoInmueble, nombre=kwargs["tipo"])
        campos = CampoTipoInmueble.objects.filter(tipo_inmueble=tipo)
        ValorCampoTipoInmuebleFormset = inlineformset_factory(Inmueble,
                                                              ValorCampoTipoInmueble,
                                                              extra=campos.count(),
                                                              can_delete=False,
                                                              fields=['campo', 'valor'])
        campotipo_formset = ValorCampoTipoInmuebleFormset(self.request.POST)
        for formset in campotipo_formset:
            formset.fields['campo'].choices = campos.values_list('id', 'nombre')
        imagen_formset = ImagenFormset(self.request.POST)
        campo_formset = CampoFormset(self.request.POST)
        if (form.is_valid() and imagen_formset.is_valid() and campo_formset.is_valid() and campotipo_formset.is_valid()):
            return self.form_valid(form, campotipo_formset, imagen_formset, campo_formset, tipo, kwargs["pais"])
        else:
            return self.form_invalid(form, campotipo_formset, imagen_formset, campo_formset, kwargs["pais"])

    def form_valid(self, form, campotipo_formset, imagen_formset, campo_formset, tipo, pais):
        self.object = form.save(commit=False)
        self.object.pais = Pais.objects.get(nombre=pais)
        self.object.tipo = tipo
        self.object.fecha_expiracion = datetime.now()
        self.object.save()
        campotipo_formset.instance = self.object
        campotipo_formset.save()
        imagen_formset.instance = self.object
        imagen_formset.save()
        campo_formset.instance = self.object
        campo_formset.save()
        return redirect('inmuebles:home_pais', pais=pais)

    def form_invalid(self, form, campotipo_formset, imagen_formset, campo_formset, pais):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  campotipo_formset=campotipo_formset,
                                  imagen_formset=imagen_formset,
                                  campo_formset=campo_formset,
                                  pais=pais))
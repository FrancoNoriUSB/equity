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
from inmuebles.models import Inmueble
from datetime import datetime, date
from django.forms.models import inlineformset_factory
from django.db.models import Count
from django.db.models import Q
from inmuebles.models import Inmueble, ValorCampoInmueble, ImagenInmueble, ValorCampoTipoInmueble, TipoInmueble, CampoTipoInmueble
from noticias.models import *
from functions import *
from django.core.mail.message import EmailMessage
from .forms import InmuebleForm
from django import forms


# Vista del index o home
def index(request):
    ctx = {
    }
    return render_to_response('index/index.html', ctx, context_instance=RequestContext(request))


def home(request, pais):
    ctx = {

    }

    return render_to_response('home/home.html', ctx, context_instance=RequestContext(request))


def inmueble(request, codigo, titulo):
    ctx = {

    }

    return render_to_response('inmuebles/inmueble.html', ctx, context_instance=RequestContext(request))


class ElegirTipo(TemplateView):
    template_name = "inmuebles/elegir-tipo.html"


class Publicar(CreateView):
    template_name = 'inmuebles/publicar.html'
    model = Inmueble
    form = InmuebleForm
    fields = '__all__'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        tipo = get_object_or_404(TipoInmueble, nombre=kwargs["tipo"])
        campos = CampoTipoInmueble.objects.filter(tipo_inmueble=tipo)
        ValorCampoTipoInmuebleFormset = inlineformset_factory(Inmueble, ValorCampoTipoInmueble, extra=campos.count(), can_delete=True)
        campotipo_formset = ValorCampoTipoInmuebleFormset()
        for formset in campotipo_formset:
            formset.fields['campo'] = forms.ChoiceField(campos.values_list('id', 'nombre'))
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        imagen_formset = inlineformset_factory(Inmueble, ImagenInmueble, extra=1, can_delete=True)
        campo_formset = inlineformset_factory(Inmueble, ValorCampoInmueble, extra=1, can_delete=True)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  campotipo_formset=campotipo_formset,
                                  imagen_formset=imagen_formset,
                                  campo_formset=campo_formset))
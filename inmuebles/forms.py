# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import inlineformset_factory, modelformset_factory, modelform_factory, BaseModelFormSet
from .models import Inmueble, ValorCampoTipoInmueble, ValorCampoInmueble, ImagenInmueble


class InmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        exclude = ['tipo']

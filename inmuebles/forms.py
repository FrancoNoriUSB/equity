# -*- coding: utf-8 -*-
from django.forms import ModelForm, Textarea
from django import forms
from models import *
from django.forms.extras.widgets import *
from django.contrib.auth.forms import UserCreationForm
from django_countries import countries

class PaisesForm(forms.Form):
    
    paises_choices = []

    paises = Pais.objects.all().order_by('nombre')

    for pais in paises:
    	paises_choices.append(((dict(countries)[pais.nombre]), (dict(countries)[pais.nombre])))

    pais = forms.ChoiceField(choices=paises_choices, required=True, widget=forms.Select(attrs={'class':"form-control"}))
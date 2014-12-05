# -*- coding: utf-8 -*-
from django.forms import ModelForm, Textarea
from django import forms
from models import *
from django.forms.extras.widgets import *
from django.contrib.auth.forms import UserCreationForm
from django_countries import countries

#Formulario para cambiar los paises en la pagina
class PaisesForm(forms.Form):
    
    paises_choices = []

    paises = Pais.objects.all().order_by('nombre')
        
    paises_choices.append(('', '- Pais -'))
    for pais in paises:
    	paises_choices.append((pais.nombre, (dict(countries)[pais.nombre])))

    pais = forms.ChoiceField(choices=paises_choices, required=True, widget=forms.Select(attrs={'class':"form-control"}))


#Formulario de busqueda de inmuebles
class BuscadorForm(forms.Form):

    ordenes = (
        ('','- Ordenar Por -'),
        ('zona','Zona'),
        ('tipo','Tipo'),
        ('precio','Precio'),
    )

    ciudad = forms.ModelChoiceField(queryset=Ciudad.objects.all(), empty_label=' - Ciudad -')
    zona = forms.ModelChoiceField(queryset=Zona.objects.all(), empty_label=' - Zona -')
    tipo = forms.ModelChoiceField(queryset=TipoInmueble.objects.all(), empty_label=' - Tipo -')
    orden = forms.ChoiceField(choices=ordenes)
    codigo = forms.CharField(max_length=12)
    palabra = forms.CharField(max_length=20)
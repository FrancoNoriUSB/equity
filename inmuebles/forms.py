# -*- coding: utf-8 -*-
from django import forms
from models import *
from django.forms.extras.widgets import *
from django.contrib.auth.forms import UserCreationForm
from django_countries import countries
from django.forms.models import inlineformset_factory


#Formulario para cambiar los paises en la pagina
class PaisesForm(forms.Form):
    
    paises_choices = []

    paises = Pais.objects.all().order_by('nombre')

    paises_choices.append(('', '- Pais -'))
    for pais in paises:
        paises_choices.append((pais.nombre, (dict(countries)[pais.nombre])))

    pais = forms.ChoiceField(choices=paises_choices, required=True, widget=forms.Select(attrs={'class': "form-control"}))


#Formulario de busqueda de inmuebles
class BuscadorForm(forms.Form):

    ordenes = (
        ('', '- Ordenar Por -'),
        ('zona', 'Zona'),
        ('tipo', 'Tipo'),
        ('precio', 'Precio'),
    )

    ciudad = forms.ModelChoiceField(queryset=Ciudad.objects.all(), empty_label=' - Ciudad -')
    zona = forms.ModelChoiceField(queryset=Zona.objects.all(), empty_label=' - Zona -')
    tipo = forms.ModelChoiceField(queryset=TipoInmueble.objects.all(), empty_label=' - Tipo -')
    orden = forms.ChoiceField(choices=ordenes)
    codigo = forms.CharField(max_length=12)
    palabra = forms.CharField(max_length=20)


#Formulario de contacto
class ContactoAgenteForm(forms.Form):

    nombre = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Nombre y Apellido'}))
    correo = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Correo'}))
    telefonos = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Teléfonos'}))
    pais = forms.ModelChoiceField(queryset=Pais.objects.all())
    ciudad = forms.ModelChoiceField(queryset=Ciudad.objects.all())
    comentario = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'placeholder': 'comentarios'}))


class InmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        widgets = {
            'latitud': forms.HiddenInput(),
            'longitud': forms.HiddenInput()
        }
        exclude = ['tipo', 'pais']


ImagenFormset = inlineformset_factory(Inmueble, ImagenInmueble, extra=5, can_delete=True, fields=['imagen', 'descripcion'])
CampoFormset = inlineformset_factory(Inmueble, ValorCampoInmueble, extra=3, can_delete=True, fields=['campo', 'valor'])

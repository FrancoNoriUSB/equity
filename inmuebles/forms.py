# -*- coding: utf-8 -*-
from django import forms
from models import *
from django.forms.extras.widgets import *
from django.contrib.auth.forms import UserCreationForm
from django_countries import countries
from django.forms.models import inlineformset_factory

#Formulario para el login de usuario                
class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username','password')
        widgets = {
            'password': forms.PasswordInput(attrs={'class':"form-control", 'placeholder':"Contraseña"}),
            'username': forms.TextInput(attrs={'class':"form-control", 'placeholder':"Usuario"}),
        }

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


#Formulario para agregar inmuebles
class InmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        widgets = {
            'fecha_entrega': forms.DateInput(),
            'latitud': forms.HiddenInput(),
            'longitud': forms.HiddenInput()
        }
        labels = {
            'descripcion': 'Descripción',
            'direccion': 'Dirección',
        }
        exclude = ['tipo', 'pais', 'fecha_expiracion']

ImagenFormset = inlineformset_factory(Inmueble, ImagenInmueble, extra=5, can_delete=True, fields=['imagen', 'descripcion'])
CampoFormset = inlineformset_factory(Inmueble, ValorCampoInmueble, extra=1, can_delete=True, fields=['campo', 'valor'])


#Formulario de registro simple de usuario
class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirme Contraseña')

    class Meta:
        model = User
        fields = ('email', 'username', 'password',)
        widgets = {
            'email': forms.EmailInput(),
            'password': forms.PasswordInput(),
        }
        labels = {
            'email': 'Correo Electrónico',
            'password': 'Contraseña',
        }


#Formulario para agentes
class AgenteForm(forms.ModelForm):
    class Meta:
        model = Agente
        widgets = {
            'codigo': forms.TextInput(),
            'logo': forms.FileInput()
        }
        exclude = ['pais']


#Formulario para los telefonos de los agentes
class TelefonoAgenteForm(forms.ModelForm):
    class Meta:
        model = TelefonoAgente
        exclude = ['agente']
    

#Formulario para ciudades
class CiudadForm(forms.ModelForm):
    class Meta:
        model = Ciudad
        widgets = {
            'nombre': forms.TextInput(),
        }
        exclude = ['pais']


#Formulario para zonas
class ZonaForm(forms.ModelForm):
    class Meta:
        model = Zona
        widgets = {
            'nombre': forms.TextInput(),
            'ciudad': forms.TextInput(),
        }

class MonedaForm(forms.ModelForm):
    class Meta:
        model = Moneda
        widgets = {
            'nombre': forms.TextInput(),
        }
        exclude = ['pais']
    
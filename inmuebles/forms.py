# -*- coding: utf-8 -*-
from django import forms
from models import *
from django.forms.extras.widgets import *
from django.contrib.auth.forms import UserCreationForm
from django_countries import countries
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _


# Formulario para el login de usuario
class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'password': forms.PasswordInput(attrs={'class': "form-control", 'placeholder': "Contraseña"}),
            'username': forms.TextInput(attrs={'class': "form-control", 'placeholder': "Usuario"}),
        }


# Formulario para cambiar los paises en la pagina
class PaisesForm(forms.Form):

    paises_choices = []

    paises = Pais.objects.all().order_by('orden')

    paises_choices.append(('', u'- País -'))
    for pais in paises:
        paises_choices.append((pais.nombre, (dict(countries)[pais.nombre])))

    pais = forms.ChoiceField(choices=paises_choices, required=True, widget=forms.Select(attrs={'class': "form-control"}))


# Formulario de busqueda de inmuebles
class BuscadorForm(forms.Form):

    ordenes = (
        ('', '- Ordenar Por -'),
        ('zona', 'Zona'),
        ('tipo', 'Tipo'),
        ('precio', 'Precio'),
    )

    habitaciones = (
        ('', ' - Habitaciones - '),
        ('0-1', ' 0 - 1 '),
        ('2-3', ' 2 - 3'),
        ('3-100', u' 3 o más '),
    )

    metros = (
        ('', ' - Metros² - '),
        ('0-50', ' 0 - 50 '),
        ('50-100', ' 50 - 100 '),
        ('100-300', ' 100 - 300 '),
        ('300-500', ' 300 - 500 '),
        ('500-1000000000', u' 500 - más '),
    )

    inmuebles = (
        # ('6', '6'),
        ('12', '12'),
        ('24', '24'),
        ('48', '48'),
    )

    monedas = (
        ('', ' - Moneda - '),
        ('nacional', 'Nacional'),
        ('usd', 'USD'),
    )

    ciudad = forms.ModelChoiceField(queryset=Ciudad.objects.all().order_by('nombre'), empty_label=' - Ciudad -', required=False)
    zona = forms.ModelChoiceField(queryset=Zona.objects.all().order_by('nombre'), empty_label=' - Zona -', required=False)
    tipo = forms.ModelChoiceField(queryset=TipoInmueble.objects.all().order_by('nombre'), empty_label=' - Tipo -', required=False)
    habitaciones = forms.ChoiceField(choices=habitaciones, required=False)
    metros = forms.ChoiceField(choices=metros, required=False)
    moneda = forms.ChoiceField(choices=monedas, required=False)
    desde = forms.CharField(max_length=15, required=False)
    hasta = forms.CharField(max_length=25, required=False)
    orden = forms.ChoiceField(choices=ordenes, required=False)
    inmuebles_inf = forms.ChoiceField(choices=inmuebles, required=False)
    inmuebles_sup = forms.ChoiceField(choices=inmuebles, required=False)
    palabra = forms.CharField(max_length=20, required=False)


# Formulario de contacto
class ContactoAgenteForm(forms.Form):

    nombre = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Nombre y Apellido', 'class': "form-control"}))
    correo = forms.CharField(max_length=50, widget=forms.EmailInput(attrs={'placeholder': 'Correo', 'class': "form-control"}))
    telefonos = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Teléfonos', 'class': "form-control"}))
    comentario = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'placeholder': 'Comentarios', 'class': "form-control"}))


# Formulario para agregar inmuebles
class InmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        widgets = {
            'fecha_entrega': forms.DateInput(),
            'latitud': forms.HiddenInput(),
            'longitud': forms.HiddenInput(),
        }
        labels = {
            'pagina': _(u'Página'),
            'descripcion': u'Descripción',
            'direccion': u'Dirección',
            'ficha_tecnina': u'Ficha Técnica',
        }
        exclude = ['tipo', 'pais', 'fecha_expiracion', 'slug']


# Formulario de imagenes de inmuebles
class ImagenInmuebleForm(forms.ModelForm):
    class Meta:
        model = ImagenInmueble
        exclude = ['inmueble']
        widgets = {
            'descripcion': forms.TextInput(),
        }


# Formulario de registro simple de usuario
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


# Formulario para agentes
class AgenteForm(forms.ModelForm):
    correo2 = forms.CharField(required=False)

    class Meta:
        model = Agente
        widgets = {
            'pagina': forms.TextInput(),
            'logo': forms.FileInput()
        }
        exclude = ['pais']


# Formulario para los telefonos de los agentes
class TelefonoAgenteForm(forms.ModelForm):
    class Meta:
        model = TelefonoAgente
        exclude = ['agente']


# Formulario para ciudades
class CiudadForm(forms.ModelForm):
    class Meta:
        model = Ciudad
        widgets = {
            'nombre': forms.TextInput(),
        }
        exclude = ['pais']


# Formulario para zonas
class ZonaForm(forms.ModelForm):
    class Meta:
        model = Zona
        widgets = {
            'nombre': forms.TextInput(),
            'ciudad': forms.TextInput(),
        }
        exclude = ['pais']


# Formulario de monedas
class MonedaForm(forms.ModelForm):
    class Meta:
        model = Moneda
        widgets = {
            'nombre': forms.TextInput(),
        }
        exclude = ['pais']


# Formulario de areas comunes
class AreaComunForm(forms.ModelForm):
    class Meta:
        model = AreaComun
        widgets = {
            'nombre': forms.TextInput(),
        }
        fields = ['nombre']
        labels = {
            'nombre': 'Otra área común',
        }

# -*- coding: utf-8 -*-
from django import forms
from models import *
from django.forms.extras.widgets import *
from django_countries import countries
from django.utils.translation import ugettext_lazy as _


# Formulario para el login de usuario
class LoginForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario', widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'placeholder': "Contraseña"}))

    def clean(self):
        cleaned_data = self.cleaned_data
        username = self.data['username']

        usuario = User.objects.filter(username=username)

        if not usuario:
            raise forms.ValidationError("Usuario inválido. ¡Introduzca un usuario existente!")
        else:
            return cleaned_data


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
    palabra = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'placeholder': 'Búsqueda'}))


# Formulario de contacto
class ContactoAgenteForm(forms.Form):

    nombre = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Nombre y Apellido', 'class': "form-control"}))
    correo = forms.CharField(max_length=50, widget=forms.EmailInput(attrs={'placeholder': 'Correo', 'class': "form-control"}))
    telefonos = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Teléfonos', 'class': "form-control"}))
    comentario = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'placeholder': 'Comentarios', 'class': "form-control"}))


# Formulario para solicitar citas
class SolicitarVisitaForm(forms.Form):

    nombre = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Nombre y Apellido', 'class': "form-control"}))
    correo = forms.CharField(max_length=50, widget=forms.EmailInput(attrs={'placeholder': 'Correo', 'class': "form-control"}))
    telefonos = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Teléfonos', 'class': "form-control"}))
    fecha_cita = forms.CharField(max_length=200, widget=forms.DateInput(attrs={'placeholder': 'Fecha visita', 'class': "form-control"}))


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


# Formulario del thumbnail del inmueble
class ThumbInmuebleForm(forms.ModelForm):
    class Meta:
        model = ThumbInmueble
        exclude = ['inmueble', 'descripcion', 'principal']


# Formulario de registro simple de usuario
class UserForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repetir contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'email', 'username',)
        widgets = {
            'email': forms.EmailInput(),
        }

        labels = {
            'first_name': 'Nombre y Apellido',
            'email': 'Correo Electrónico',
            'username': 'Nombre de Usuario',
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# Formulario de registro simple de usuario
class EditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'email',)
        widgets = {
            'email': forms.EmailInput(),
        }

        labels = {
            'first_name': 'Nombre',
            'email': 'Correo Electrónico',
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

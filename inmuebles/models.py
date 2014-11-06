# -*- coding: utf-8 -*-
from django.utils.translation import gettext as _
from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User


# Pais al cual pertenece el usuario de Perfil
class Pais(models.Model):
    #Campos del pais
    nombre = CountryField()

    class Meta:
        verbose_name = _('Pais')
        verbose_name_plural = _('Paises')

    def __unicode__(self):
        return self.nombre


#Ciudad que se relaciona con el pais
class Ciudad(models.Model):
    #Campos para la ciudad
    nombre = models.CharField(max_length=80)

    #Claves foraneas
    pais = models.ForeignKey(Pais)

    class Meta:
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"

    def __unicode__(self):
        return self.nombre


#Zona que se relaciona con la ciudad
class Zona(models.Model):
    #Campos para la ciudad
    nombre = models.CharField(max_length=80)

    #Claves foraneas
    ciudad = models.ForeignKey(Ciudad)

    class Meta:
        verbose_name = "Zona"
        verbose_name_plural = "Zonas"

    def __unicode__(self):
        return self.nombre


class Agente(models.Model):
    usuario = models.OneToOneField(User)
    codigo = models.CharField(max_length=40)
    pais = models.ForeignKey(Pais)
    logo = models.ImageField()

    def __unicode__(self):
        return self.usuario


class Telefono(models.Model):
    agente = models.ForeignKey(Agente)
    telefono = models.CharField(max_length=50)


# Modelo para los distintos tipo de inmuebles que se pueden publicar
class TipoInmueble(models.Model):
    nombre = models.CharField(max_length=80)


# Modelo para definir los campos bases para cada tipo de inmueble
class CampoTipoInmueble(models.Model):
    NUMERO = 'N'
    TEXTO = 'T'
    TIPOS = (
        (NUMERO, 'Número'),
        (TEXTO, 'Texto'),
    )
    nombre = models.CharField(max_length=80)
    tipo = models.CharField(max_length=1, choices=TIPOS, default=TEXTO)
    tipo_actividad = models.ForeignKey(TipoInmueble)


# Modelo para los valores de los campos de cada inmueble publicado
class ValorCampoTipoInmueble(models.Model):
    valor = models.CharField(max_length=150)
    campo = models.ForeignKey(CampoTipoInmueble)
    inmueble = models.ForeignKey(Inmueble)


# Modelo para cada inmueble publicado
class Inmueble(models.Model):
    titulo = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20)
    descripcion = models.TextField()
    pais = models.ForeignKey(Pais)
    ciudad = models.ForeignKey(Ciudad)
    zona = models.ForeignKey(Zona)
    direccion = models.CharField(max_length=150)
    agente = models.ForeignKey(Agente)
    tipo = models.ForeignKey(TipoInmueble)
    # Coodenadas Google Maps
    latitud = models.DecimalField(max_digits=8, decimal_places=6)
    longitud = models.DecimalField(max_digits=8, decimal_places=6)

    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    feche_actualizacion = models.DateTimeField(auto_now=True)
    fecha_expiracion = models.DateTimeField()


# Modelo para imágenes de un inmueble publicado
class Imagen(models.Model):
    imagen = models.ImageField()
    inmueble = models.ForeignKey(Inmueble)


# Modelo para los campos propios de cada inmueble publicado
class CampoInmueble(models.Model):
    nombre = models.CharField(max_length=20)
    valor = models.CharField(max_length=20)
    inmueble = models.ForeignKey(Inmueble)
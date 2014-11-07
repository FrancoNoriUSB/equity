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
        return u"%s" % self.nombre


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
        return u"%s" % self.nombre


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
        return u"%s" % self.nombre


class Agente(models.Model):
    codigo = models.CharField(max_length=40)
    logo = models.ImageField()
    usuario = models.OneToOneField(User)
    pais = models.ForeignKey(Pais)

    def __unicode__(self):
        return u"%s" % self.usuario


class Telefono(models.Model):
    telefono = models.CharField(max_length=50)
    agente = models.ForeignKey(Agente)

    def __unicode__(self):
        return u"%s" % self.telefono


# Modelo para los distintos tipo de inmuebles que se pueden publicar
class TipoInmueble(models.Model):
    nombre = models.CharField(max_length=80)

    def __unicode__(self):
        return u"%s" % self.nombre


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
    tipo_inmueble = models.ForeignKey(TipoInmueble)

    def __unicode__(self):
        return u"%s" % self.nombre


# Modelo para cada inmueble publicado
class Inmueble(models.Model):
    titulo = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20)
    descripcion = models.TextField()
    direccion = models.CharField(max_length=150)
    # Coodenadas Google Maps
    latitud = models.DecimalField(max_digits=8, decimal_places=6)
    longitud = models.DecimalField(max_digits=8, decimal_places=6)

    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    feche_actualizacion = models.DateTimeField(auto_now=True)
    fecha_expiracion = models.DateTimeField()

    pais = models.ForeignKey(Pais)
    ciudad = models.ForeignKey(Ciudad)
    zona = models.ForeignKey(Zona)
    agente = models.ForeignKey(Agente)
    tipo = models.ForeignKey(TipoInmueble)

    def __unicode__(self):
        return u"%s" % self.titulo


# Modelo para los valores de los campos de cada inmueble publicado
class ValorCampoTipoInmueble(models.Model):
    valor = models.CharField(max_length=150)
    campo = models.ForeignKey(CampoTipoInmueble)
    inmueble = models.ForeignKey(Inmueble)

    def __unicode__(self):
        return u"%s" % self.valor


# Modelo para imágenes de un inmueble publicado
class Imagen(models.Model):
    imagen = models.ImageField()
    thumbnail = models.ImageField()
    inmueble = models.ForeignKey(Inmueble)


class CampoInmueble(models.Model):
    NUMERO = 'N'
    TEXTO = 'T'
    TIPOS = (
        (NUMERO, 'Número'),
        (TEXTO, 'Texto'),
    )
    nombre = models.CharField(max_length=80)
    tipo = models.CharField(max_length=1, choices=TIPOS, default=TEXTO)


# Modelo para los campos propios de cada inmueble publicado
class ValorCampoInmueble(models.Model):
    valor = models.CharField(max_length=20)
    campo = models.ForeignKey(CampoInmueble)
    inmueble = models.ForeignKey(Inmueble)

    def __unicode__(self):
        return u"%s - %s" % self.nombre, self.valor
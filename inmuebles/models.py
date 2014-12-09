# -*- coding: utf-8 -*-
import os
from Equity.settings import *
from django.utils.translation import gettext as _
from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User


# Pais al cual pertenece el usuario de Perfil
class Pais(models.Model):
    # Campos del pais
    nombre = CountryField()

    class Meta:
        verbose_name = _('Pais')
        verbose_name_plural = _('Paises')

    def __unicode__(self):
        return unicode(self.nombre)


# Ciudad que se relaciona con el pais
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


#Imagen de los anuncios que se publican
class Imagen(models.Model):
    imagen = models.ImageField(upload_to='uploads/img/')
    thumbnail = models.ImageField(upload_to='uploads/img/thumbnails/', blank=True, null=True, editable=False)
    descripcion = models.CharField(max_length=140, null=True)

    #Metodo para crear el thumbnail al momento de cear la imagen
    def create_thumbnail(self):
        # If there is no image associated with this.
        # do not create thumbnail
        if not self.imagen:
            return

        from PIL import Image
        from cStringIO import StringIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os

        # Set our max thumbnail size in a tuple (max width, max height)
        THUMBNAIL_SIZE = (200, 200)

        # Open original photo which we want to thumbnail using PIL's Image
        imagen = Image.open(StringIO(self.imagen.read()))
        image_type = imagen.format.lower()

        imagen.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        # Save the thumbnail
        temp_handle = StringIO()
        imagen.save(temp_handle, image_type)
        temp_handle.seek(0)

        # Save image to a SimpleUploadedFile which can be saved into
        # ImageField
        suf = SimpleUploadedFile(os.path.split(self.imagen.name)[-1], temp_handle.read(),
                                 content_type='imagen/%s' % (image_type))
        # Save SimpleUploadedFile into image field
        self.thumbnail.save('%s_thumbnail.%s' %
                            (os.path.splitext(suf.name)[0], image_type), suf, save=False)

    def save(self):
        # create a thumbnail
        self.create_thumbnail()

        super(Imagen, self).save()

    class Meta:
        abstract = True
        ordering = ('imagen',)
        verbose_name = _('Imagen')
        verbose_name_plural = _('Imagenes')

    def __unicode__(self):
        return self.descripcion


#Modelo para el Agente inmobiliario
class Agente(models.Model):
    usuario = models.OneToOneField(User)
    codigo = models.CharField(max_length=40)
    pais = models.ForeignKey(Pais)
    logo = models.ImageField(upload_to='agentes/')

    class Meta:
        verbose_name = "Agente"
        verbose_name_plural = "Agentes"

    def __unicode__(self):
        return self.usuario.username


#Clase abstracta de Telefonos
class Telefono(models.Model):
    numero = models.CharField(max_length=30)

    class Meta:
        abstract = True
        verbose_name = _('Telefono')
        verbose_name_plural = _('Telefonos')

    def __unicode__(self):
        return self.numero


# Modelo para los telefonos del agente
class TelefonoAgente(Telefono):
    agente = models.ForeignKey(Agente, related_name='telefonos')

    class Meta(Telefono.Meta):
        verbose_name = _('Telefono Agente')
        verbose_name_plural = _('Telefonos Agentes')
        abstract = False


# Modelo para los distintos tipo de inmuebles que se pueden publicar
class TipoInmueble(models.Model):
    nombre = models.CharField(max_length=80)

    class Meta:
        verbose_name = "Tipo Inmueble"
        verbose_name_plural = "Tipos Inmuebles"

    def __unicode__(self):
        return self.nombre


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
    latitud = models.DecimalField(max_digits=12, decimal_places=10)
    longitud = models.DecimalField(max_digits=12, decimal_places=10)

    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    feche_actualizacion = models.DateTimeField(auto_now=True)
    fecha_expiracion = models.DateTimeField()

    class Meta:
        verbose_name = "Inmueble"
        verbose_name_plural = "Inmuebles"

    def __unicode__(self):
        return self.titulo


# Modelo para imágenes de un inmueble publicado
class ImagenInmueble(Imagen):
    inmueble = models.ForeignKey(Inmueble)

    def __unicode__(self):
        return self.descripcion


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

    class Meta:
        verbose_name = "Campo Tipo Inmueble"
        verbose_name_plural = "Campos Tipo Inmueble"

    def __unicode__(self):
        return self.nombre


# Modelo para los valores de los campos de cada inmueble publicado
class ValorCampoTipoInmueble(models.Model):
    valor = models.CharField(max_length=150)
    campo = models.ForeignKey(CampoTipoInmueble)
    inmueble = models.ForeignKey(Inmueble)

    class Meta:
        verbose_name = "Valor Campo Tipo Inmueble"
        verbose_name_plural = "Valor Campos Tipo Inmueble"

    def __unicode__(self):
        return self.valor


# Modelo para los campos propios de cada inmueble publicado
class CampoInmueble(models.Model):
    NUMERO = 'N'
    TEXTO = 'T'
    TIPOS = (
        (NUMERO, 'Número'),
        (TEXTO, 'Texto'),
    )
    nombre = models.CharField(max_length=80)
    tipo = models.CharField(max_length=1, choices=TIPOS, default=TEXTO)

    class Meta:
        verbose_name = "Campo Inmueble"
        verbose_name_plural = "Campos Inmueble"

    def __unicode__(self):
        return self.nombre


class ValorCampoInmueble(models.Model):
    valor = models.CharField(max_length=150)
    campo = models.ForeignKey(CampoInmueble)
    inmueble = models.ForeignKey(Inmueble)

    class Meta:
        verbose_name = "Valor Campo Inmueble"
        verbose_name_plural = "Valor Campos Inmueble"

    def __unicode__(self):
        return self.valor
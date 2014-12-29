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
    principal = models.BooleanField(default=True, help_text='Marcado si desea que se muestre como imagen principal')

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
    nombre = models.CharField(max_length=30)
    correo = models.CharField(max_length=40)
    logo = models.ImageField(upload_to='agentes/')

    #Claves foraneas
    pais = models.ForeignKey(Pais)

    class Meta:
        verbose_name = "Agente"
        verbose_name_plural = "Agentes"

    def __unicode__(self):
        return self.nombre


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

    tipo = models.CharField(max_length=20, choices=(('Celular','Celular'),('Local','Local')))
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


# Modelo para las areas comunes
class AreaComun(models.Model):
    nombre = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Area Comun"
        verbose_name_plural = "Area Comunes"

    def __unicode__(self):
        return self.nombre


# Modelo para cada inmueble publicado
class Inmueble(models.Model):

    tipos_obra = (
        ('Pre-venta','Pre-venta'),
        ('En Construccion', u'En Construcción'),
        ('Listo por entregar','Listo Para Entregar'),
    )

    titulo = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.TextField()
    fecha_entrega = models.DateField()
    tipo_obra = models.CharField(choices=tipos_obra, max_length=20)
    direccion = models.CharField(max_length=150)
    latitud = models.DecimalField(max_digits=20, decimal_places=17)
    longitud = models.DecimalField(max_digits=20, decimal_places=17)
    logo = models.ImageField(upload_to='logos_inmuebles/')
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    feche_actualizacion = models.DateTimeField(auto_now=True)
    fecha_expiracion = models.DateTimeField()
    
    #Claves foraneas
    pais = models.ForeignKey(Pais)
    ciudad = models.ForeignKey(Ciudad)
    zona = models.ForeignKey(Zona)
    agente = models.ForeignKey(Agente)
    tipo = models.ForeignKey(TipoInmueble)
    areas_comunes = models.ManyToManyField(AreaComun)

    class Meta:
        verbose_name = "Inmueble"
        verbose_name_plural = "Inmuebles"

    def __unicode__(self):
        return self.titulo


# Modelo para imágenes de un inmueble publicado
class ImagenInmueble(Imagen):
    inmueble = models.ForeignKey(Inmueble, related_name='imagenes')

    def __unicode__(self):
        return self.descripcion


# Modelo para los modulos de cada inmueble
class Modulo(models.Model):

    tipo = models.CharField(max_length=30, default='A')
    metros = models.CharField(max_length=10)
    banos = models.CharField(max_length=2)
    dormitorios = models.CharField(max_length=2)
    estacionamientos = models.CharField(max_length=2)
    precio = models.CharField(max_length=10)
    plano = models.ImageField(upload_to='uploads/planos/')

    #Claves foraneas
    inmueble = models.ForeignKey(Inmueble)

    class Meta:
        verbose_name = "Modulo"
        verbose_name_plural = "Modulos"

    def __unicode__(self):
        return self.nombre


# Modelo para las monedas
class Moneda(models.Model):
    nombre = models.CharField(max_length=20)
    tasa = models.DecimalField(max_digits=20, decimal_places=4)

    #Claves foraneas
    pais = models.OneToOneField(Pais)

    class Meta:
        verbose_name = "Moneda"
        verbose_name_plural = "Monedas"

    def __unicode__(self):
        return self.nombre


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

    #Claves foraneas
    tipo_inmueble = models.ForeignKey(TipoInmueble)

    class Meta:
        verbose_name = "Campo Tipo Inmueble"
        verbose_name_plural = "Campos Tipo Inmueble"

    def __unicode__(self):
        return self.nombre


# Modelo para los valores de los campos de cada inmueble publicado
class ValorCampoTipoInmueble(models.Model):
    valor = models.CharField(max_length=150)

    #Claves foraneas
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


# Modelo para los valores de los campos opcionales de los inmuebles
class ValorCampoInmueble(models.Model):
    valor = models.CharField(max_length=150)

    #Claves foraneas
    campo = models.ForeignKey(CampoInmueble)
    inmueble = models.ForeignKey(Inmueble)

    class Meta:
        verbose_name = "Valor Campo Inmueble"
        verbose_name_plural = "Valor Campos Inmueble"

    def __unicode__(self):
        return self.valor


# Modelo para las imagenes de los Slides del home
class Slide(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='slide-home/')

    #Claves foraneas
    pais = models.ForeignKey(Pais)

    class Meta:
        verbose_name = "Slide"
        verbose_name_plural = "Slides"

    def __unicode__(self):
        return self.nombre


# Modelo para los banners publicitarios
class Banner(models.Model):
    posiciones = (
        ('Superior','Superior'),
        ('Medio-Superior','Medio-Superior'),
        ('Medio-Inferior','Medio-Inferior'),
        ('Inferior','Inferior'),
    )

    nombre = models.CharField(max_length=100, choices=posiciones)
    imagen = models.ImageField(upload_to='slide-home/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    #Claves foraneas
    pais = models.ForeignKey(Pais)

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"

    def __unicode__(self):
        return self.nombre

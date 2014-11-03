# -*- coding: utf-8 -*-
from django.utils.translation import gettext as _
from django.db import models
from django.contrib.auth.models import User
from inmuebles.models import *

#Modelos de las noticias que publican los usuarios.

#Tobla para los usuarios que postean noticias y realizan operaciones varias
class Usuario(models.Model):

	#Campos de los usuarios
	identificador = models.CharField(max_length=20)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)	

	#Claves foraneas
	user = models.ForeignKey(User)    

	class Meta:
		ordering = ('user',)
		verbose_name = _('Usuario')
		verbose_name_plural = _('Usuarios')

	def __unicode__(self):
		return u"%s" %(self.identificador)

#Tabla para las noticias
class Noticia(models.Model):

	#Campos de las noticias
	titulo = models.CharField(max_length=80, null=False)
	cuerpo = models.TextField(max_length=6000)
	imagen = models.ImageField(upload_to='')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	#Claves foraneas
	autor = models.ForeignKey(Usuario)

	class Meta:
		ordering = ('created_at',)
		verbose_name = _('Noticia')
		verbose_name_plural = _('Noticias')

	def __unicode__(self):
		return u"%s" %(self.titulo)

#Tabla para los banners
class Banner(models.Model):

	#Campos de las noticias
	imagen = models.ImageField(upload_to='')
	posicion = models.CharField(max_length=50)

	#Claves foraneas
	pais = models.ForeignKey(Pais)

	class Meta:
		ordering = ('pais',)
		verbose_name = _('Banner')
		verbose_name_plural = _('Banners')

	def __unicode__(self):
		return u"%s" %(self.posicion)
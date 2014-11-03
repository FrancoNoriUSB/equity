# -*- coding: utf-8 -*-
from django.utils.translation import gettext as _
from django.db import models
from django_countries.fields import CountryField
# Create your models here.

#Pais al cual pertenece el usuario de Perfil
class Pais(models.Model):

	#Campos del pais
	nombre = CountryField()

	class Meta:
		verbose_name = _('Pais')
		verbose_name_plural = _('Paises')

	def __unicode__(self):
		return self.nombre.name

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
		pass
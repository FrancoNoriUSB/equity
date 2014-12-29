# -*- coding: utf-8 -*-
from django.utils.translation import gettext as _
from django.db import models
from django.contrib.auth.models import User
from inmuebles.models import Pais


#Tabla para las noticias
class Noticia(models.Model):
    #Campos de la noticia
    titulo = models.CharField(max_length=80, null=False)
    cuerpo = models.TextField(max_length=6000)
    imagen = models.ImageField(upload_to='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #Claves foraneas
    autor = models.ForeignKey(User)
    pais = models.ForeignKey(Pais)

    class Meta:
        ordering = ('created_at',)
        verbose_name = _('Noticia')
        verbose_name_plural = _('Noticias')

    def __unicode__(self):
        return u"%s" % self.titulo

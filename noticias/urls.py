from django.conf.urls import *

#Urls para los views del frontend del usuario visitante
urlpatterns = patterns('noticias.views',
	url(r'^noticia/$', 'noticia', name='noticia'),
)
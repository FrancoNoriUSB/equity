from django.conf.urls import *
from django.conf import settings

#Urls para los views del frontend del usuario visitante
urlpatterns = patterns('inmuebles.views',
	url(r'^$', 'index', name='pre_home'),
	url(r'^pais/(?P<pais>.*)/$', 'home', name='home_pais'),
	url(r'^inmueble/(?P<codigo>.*)-(?P<titulo>.*)$', 'inmueble', name='inmueble'),
)
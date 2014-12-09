from django.conf.urls import *
from inmuebles.views import ElegirTipo, Publicar
from django.conf import settings

# Urls para los views del frontend del usuario visitante
urlpatterns = patterns('inmuebles.views',
                       url(r'^$', 'index', name='pre_home'),
                       url(r'^pais/(?P<pais>.*)/$', 'home', name='home_pais'),
                       url(r'^inmuebles/(?P<codigo>.*)-(?P<titulo>.*)$', 'inmueble', name='inmueble'),
                       url(r'^inmuebles/elegir-tipo', ElegirTipo.as_view(), name='elegir_tipo'),
                       url(r'^inmuebles/publicar/(?P<tipo>.*)$', Publicar.as_view(), name='publicar'),
)
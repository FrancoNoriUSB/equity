from django.conf.urls import *
from inmuebles.views import ElegirTipo, Publicar
from django.conf import settings

#Urls para los views del frontend del usuario visitante
urlpatterns = patterns('inmuebles.views',
                       url(r'^(?P<pais>[A-Z][A-Z])/$', 'home', name='home_pais'),
                       url(r'^(?P<pais>[A-Z][A-Z])/inmuebles/(?P<codigo>[A-Z][A-Z]\.[0-9]+)/$', 'inmueble', name='inmueble'),
                       url(r'^(?P<pais>[A-Z][A-Z])/inmuebles/elegir-tipo/', ElegirTipo.as_view(), name='elegir_tipo'),
                       url(r'^(?P<pais>[A-Z][A-Z])/inmuebles/publicar/(?P<tipo>.*)/$', Publicar.as_view(), name='publicar'),
)
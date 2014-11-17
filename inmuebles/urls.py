from django.conf.urls import *
from django.conf import settings

#Urls para los views del frontend del usuario visitante
urlpatterns = patterns('inmuebles.views',
    url(r'^(?P<pais>[A-Z][A-Z])/$', 'home', name='home_pais'),
    url(r'^(?P<pais>[A-Z][A-Z])/inmueble/(?P<codigo>[A-Z][A-Z]\.[0-9]+)/$', 'inmueble', name='inmueble'),
)
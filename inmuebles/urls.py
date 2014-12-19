from django.conf.urls import *
from inmuebles.views import ElegirTipo, Publicar
from django.conf import settings
from django.contrib.auth.decorators import login_required

#Urls para los views del frontend del usuario visitante
urlpatterns = patterns('inmuebles.views',
             url(r'^(?P<pais>[A-Z][A-Z])/$', 'home', name='home_pais'),
             url(r'^(?P<pais>[A-Z][A-Z])/inmuebles/(?P<codigo>[0-9A-Za-z]+)/$', 'inmueble', name='inmueble'),

                       #Vistas del admin de equity
					   url(r'^(?P<pais>[A-Z][A-Z])/admin/login/$', 'login_admin', name='login_admin'),
					   url(r'^(?P<pais>[A-Z][A-Z])/admin/perfil/logout/$', 'logout_admin', name='logout_admin'),
					   url(r'^(?P<pais>[A-Z][A-Z])/admin/perfil/$', 'perfil_admin', name='perfil_admin'),

					   #Inmuebles
             url(r'^(?P<pais>[A-Z][A-Z])/admin/inmuebles/$', 'inmuebles_list', name='listar_inmuebles'),
             url(r'^(?P<pais>[A-Z][A-Z])/admin/inmuebles/elegir-tipo/', login_required(ElegirTipo.as_view()), name='elegir_tipo'),
             url(r'^(?P<pais>[A-Z][A-Z])/admin/inmuebles/publicar/(?P<tipo>.*)/$', login_required(Publicar.as_view()), name='publicar'),

             #Agentes
             url(r'^(?P<pais>[A-Z][A-Z])/admin/agentes/$', 'agentes_list', name='listar_agentes'),
             url(r'^(?P<pais>[A-Z][A-Z])/admin/agentes/agregar$', 'agentes_agregar', name='agregar_agentes'),

             #Ciudades
             url(r'^(?P<pais>[A-Z][A-Z])/admin/ciudades/$', 'ciudades_list', name='listar_ciudades'),
             url(r'^(?P<pais>[A-Z][A-Z])/admin/ciudades/agregar$', 'ciudades_agregar', name='agregar_ciudades'),

             #Monedas
             url(r'^(?P<pais>[A-Z][A-Z])/admin/monedas/$', 'monedas_list', name='listar_monedas'),
             url(r'^(?P<pais>[A-Z][A-Z])/admin/monedas/agregar$', 'monedas_agregar', name='agregar_monedas'),

)
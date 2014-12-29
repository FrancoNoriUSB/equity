from django.conf.urls import *
from inmuebles.views import ElegirTipo, Publicar, DetalleInmueble, AgregarModulo, EditarModulo
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
            url(r'^(?P<pais>[A-Z][A-Z])/admin/inmuebles/editar/(?P<id_inmueble>[0-9A-Za-z]+)/$', 'inmuebles_editar', name='editar_inmuebles'),
            url(r'^(?P<pais>[A-Z][A-Z])/admin/inmuebles/eliminar/(?P<id_inmueble>[0-9A-Za-z]+)/$', 'inmuebles_eliminar', name='eliminar_inmuebles'),
            url(r'^(?P<pais>[A-Z][A-Z])/admin/inmuebles/detalle/(?P<id_inmueble>\d*)/$', login_required(DetalleInmueble.as_view()), name='detalle'),
            url(r'^(?P<pais>[A-Z][A-Z])/admin/inmuebles/detalle/(?P<id_inmueble>\d*)/agregar-modulo/$', login_required(AgregarModulo.as_view()), name='agregar_modulo'),
            url(r'^(?P<pais>[A-Z][A-Z])/admin/inmuebles/detalle/(?P<id_inmueble>\d*)/editar-modulo/(?P<id_modulo>\d*)/$', login_required(EditarModulo.as_view()), name='editar_modulo'),
            url(r'^(?P<pais>[A-Z][A-Z])/admin/inmuebles/detalle/(?P<id_inmueble>\d*)/eliminar-modulo/(?P<id_modulo>\d*)/$', 'modulos_eliminar', name='eliminar_modulo'),

            #Agentes
            url(r'^(?P<pais>[A-Z][A-Z])/admin/agentes/$', 'agentes_list', name='listar_agentes'),
            url(r'^(?P<pais>[A-Z][A-Z])/admin/agentes/agregar/$', 'agentes_agregar', name='agregar_agentes'),
            url(r'^(?P<pais>[A-Z][A-Z])/admin/agentes/editar/(?P<id_agente>[0-9A-Za-z]+)/$', 'agentes_editar', name='editar_agentes'),
            url(r'^(?P<pais>[A-Z][A-Z])/admin/agentes/eliminar/(?P<id_agente>[0-9A-Za-z]+)/$', 'agentes_eliminar', name='eliminar_agentes'),


            #Ciudades
            url(r'^(?P<pais>[A-Z][A-Z])/admin/ciudades/$', 'ciudades_list', name='listar_ciudades'),
            url(r'^(?P<pais>[A-Z][A-Z])/admin/ciudades/agregar/$', 'ciudades_agregar', name='agregar_ciudades'),
            url(r'^(?P<pais>[A-Z][A-Z])/admin/ciudades/editar/(?P<id_ciudad>[0-9A-Za-z]+)/$', 'ciudades_editar', name='editar_ciudades'),
            url(r'^(?P<pais>[A-Z][A-Z])/admin/ciudades/eliminar/(?P<id_ciudad>[0-9A-Za-z]+)/$', 'ciudades_eliminar', name='eliminar_ciudades'),


            #Zonas
            url(r'^(?P<pais>[A-Z][A-Z])/admin/zonas/$', 'zonas_list', name='listar_zonas'),
            url(r'^(?P<pais>[A-Z][A-Z])/admin/zonas/agregar/$', 'zonas_agregar', name='agregar_zonas'),
            url(r'^(?P<pais>[A-Z][A-Z])/admin/zonas/editar/(?P<id_zona>[0-9A-Za-z]+)/$', 'zonas_editar', name='editar_zonas'),
            url(r'^(?P<pais>[A-Z][A-Z])/admin/zonas/eliminar/(?P<id_zona>[0-9A-Za-z]+)/$', 'zonas_eliminar', name='eliminar_zonas'),


            #Monedas
            url(r'^(?P<pais>[A-Z][A-Z])/admin/monedas/$', 'monedas_list', name='listar_monedas'),
            url(r'^(?P<pais>[A-Z][A-Z])/admin/monedas/agregar/$', 'monedas_agregar', name='agregar_monedas'),
            url(r'^(?P<pais>[A-Z][A-Z])/admin/monedas/editar/(?P<id_moneda>[0-9A-Za-z]+)/$', 'monedas_editar', name='editar_monedas'),
            url(r'^(?P<pais>[A-Z][A-Z])/admin/monedas/eliminar/(?P<id_moneda>[0-9A-Za-z]+)/$', 'monedas_eliminar', name='eliminar_monedas'),

)
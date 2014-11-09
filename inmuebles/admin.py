from django.contrib import admin
from inmuebles.models import *


class ImagenInLine(admin.StackedInline):
    model = Imagen
    extra = 0


class CampoInmuebleInLine(admin.StackedInline):
    model = CampoInmueble
    extra = 0


class CampoTipoInmuebleInLine(admin.StackedInline):
    model = CampoTipoInmueble
    extra = 0


class ValorCampoTipoInLine(admin.StackedInline):
    model = ValorCampoTipoInmueble
    extra = 0


class ValorCampoInmuebleInLine(admin.StackedInline):
    model = ValorCampoTipoInmueble
    extra = 0


class TelefonoInLine(admin.StackedInline):
    model = Telefono
    extra = 0


class InmuebleAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'codigo', 'pais', 'ciudad', 'zona', 'fecha_publicacion')
    inlines = [ImagenInLine, ValorCampoInmuebleInLine, ValorCampoTipoInLine]


class AgenteAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'codigo', 'pais']
    inlines = [TelefonoInLine]


class TipoInmuebleAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    inlines = [CampoTipoInmuebleInLine]


class ImagenAdmin(admin.ModelAdmin):
    list_display = ('imagen', 'inmueble')


class CiudadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pais')


class ZonaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ciudad')


class TelefonoAdmin(admin.ModelAdmin):
    list_display = ('telefono', 'agente')


class CampoTipoInmuebleAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'tipo_inmueble')


class CampoInmuebleAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo')


class ValorCampoTipoInmuebleAdmin(admin.ModelAdmin):
    list_display = ('valor', 'campo', 'inmueble')


class ValorCampoInmuebleAdmin(admin.ModelAdmin):
    list_display = ('valor', 'campo', 'inmueble')


admin.site.register(Inmueble, InmuebleAdmin)
admin.site.register(Agente, AgenteAdmin)
admin.site.register(Imagen, ImagenAdmin)
admin.site.register(Pais)
admin.site.register(Telefono, TelefonoAdmin)
admin.site.register(TipoInmueble, TipoInmuebleAdmin)
admin.site.register(Ciudad, CiudadAdmin)
admin.site.register(Zona, ZonaAdmin)
admin.site.register(ValorCampoTipoInmueble, ValorCampoTipoInmuebleAdmin)
admin.site.register(ValorCampoInmueble, ValorCampoInmuebleAdmin)
admin.site.register(CampoTipoInmueble, CampoTipoInmuebleAdmin)
admin.site.register(CampoInmueble, CampoInmuebleAdmin)
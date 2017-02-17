# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.core.urlresolvers import reverse_lazy
from django.template import Context
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.views.generic import TemplateView, CreateView, ListView, UpdateView
from datetime import datetime, date
from django.forms.models import inlineformset_factory
from django.db.models import Count
from django.db.models import Q
from inmuebles.models import *
from inmuebles.forms import *
from noticias.models import *
from functions import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_countries import countries
from django import forms
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from easy_pdf.views import PDFTemplateView
import json
import re


# Vista del index o home
def index(request):

    # Formulario para los paises disponibles
    paisesF = PaisesForm(initial={

    })

    ctx = {
        'PaisesForm': paisesF,
    }

    return render_to_response('index/index.html', ctx, context_instance=RequestContext(request))


# Vista del home de cada pais
def home(request, pais):

    # Buscador de inmuebles
    buscadorF = BuscadorForm()

    buscadorF.fields['pais'] = forms.ModelChoiceField(Pais.objects.filter(nombre=pais), empty_label=u' - País -')
    buscadorF.fields['ciudad'] = forms.ModelChoiceField(Ciudad.objects.filter(pais__nombre=pais), empty_label=' - Ciudad -')
    buscadorF.fields['zona'] = forms.ModelChoiceField(Zona.objects.filter(ciudad__pais__nombre=pais), empty_label=' - Zona -')

    ciudades = {}
    zonas = {}
    inmuebles = []
    min_habitaciones = 0
    max_habitaciones = 0
    inmuebles_pagina = 24
    inmuebles_inf = 24
    inmuebles_sup = 24
    moneda_get = ''
    hasta = ''
    precio_min = ''
    precio_max = ''

    # Imagen del banner
    imagen_banner = Slide.objects.filter(pais__nombre=pais)[:1]

    # Lista inmuebles por pagina
    inmuebles_list = Inmueble.objects.filter(pais__nombre=pais, visible=True).order_by('ciudad__nombre', 'zona__nombre', 'tipo__nombre')

    # Moneda nacional
    try:
        moneda = Moneda.objects.get(pais__nombre=pais)
    except:
        moneda = ''

    if request.GET:
        buscadorF = BuscadorForm(request.GET)

        # Caso para el buscador de inmuebles
        if buscadorF.is_valid():
            pais = buscadorF.cleaned_data['pais']
            ciudad = buscadorF.cleaned_data['ciudad']
            zona = buscadorF.cleaned_data['zona']
            tipo = buscadorF.cleaned_data['tipo']
            habitaciones = buscadorF.cleaned_data['habitaciones']
            # orden = buscadorF.cleaned_data['orden']
            metros = buscadorF.cleaned_data['metros']
            moneda_get = buscadorF.cleaned_data['moneda']
            hasta = str(buscadorF.cleaned_data['hasta'])
            palabra = buscadorF.cleaned_data['palabra']
            inmuebles_inf = buscadorF.cleaned_data['inmuebles_inf']
            inmuebles_sup = buscadorF.cleaned_data['inmuebles_sup']

            # Revisa si las habitaciones no son vacias
            if habitaciones != '':
                habitaciones = habitaciones.split('-', 2)
                min_habitaciones = int(habitaciones[0])
                max_habitaciones = int(habitaciones[1])

            # Revisa si los metros no son vacios
            if metros != '':
                metros = metros.split('-', 2)
                metros_min = int(metros[0])
                metros_max = int(metros[1])

            # Revisa si el precio no es vacio
            if (hasta != ''):
                precio_max = int(re.sub('[,.]', '', hasta.split('.')[0]))

                if moneda_get == 'nacional':
                    precio_max = precio_max / int(moneda.tasa)
                elif moneda_get == 'usd':
                    precio_max = precio_max

                    # Verificacion de cumplimiento de limites
                    if precio_max == 0:
                        precio_max = -1
                    if precio_min == 0:
                        precio_min = 1

            # Caso de busqueda por codigo
            if palabra != '':

                slug = slugify(palabra)
                inmuebles_list = Inmueble.objects.filter(pais__nombre=pais, slug__icontains=slug, visible=True)

                if not inmuebles_list:
                    inmuebles_list = Inmueble.objects.filter(pais__nombre=pais, codigo__startswith=palabra, visible=True)
                if not inmuebles_list:
                    inmuebles_list = Inmueble.objects.filter(pais__nombre=pais, agente__nombre=slug, visible=True)

            # Caso demas
            elif (pais is not None) or (ciudad is not None) or (zona is not None) or (tipo is not None) or (habitaciones != '') or (precio_max != '') or (metros != ''):

                # Verificacion de string vacio
                # if orden == '':
                #     orden = None

                # if precio_max != '':
                #     orden = 'precio'

                # if metros != '':
                #     orden = 'metros'

                # Campos a buscar
                fields_list = []
                fields_list.append('pais')
                fields_list.append('ciudad')
                fields_list.append('zona')
                fields_list.append('tipo')
                fields_list.append('visible')

                if metros != '':
                    fields_list.append('modulo__metros')

                if habitaciones != '':
                    fields_list.append('modulo__dormitorios')

                if precio_max != '':
                    fields_list.append('modulo__precio')

                # Comparadores para buscar
                types_list = []
                types_list.append('nombre__exact')
                types_list.append('nombre__exact')
                types_list.append('nombre__exact')
                types_list.append('nombre__exact')
                types_list.append('exact')

                if metros != '':
                    types_list.append('range')

                if habitaciones != '':
                    types_list.append('range')

                if precio_max != '':
                    types_list.append('range')

                # Valores a buscar
                values_list = []
                values_list.append(pais)
                values_list.append(ciudad)
                values_list.append(zona)
                values_list.append(tipo)
                values_list.append('True')

                if metros != '':
                    values_list.append((metros_min, metros_max))

                if habitaciones != '':
                    values_list.append((min_habitaciones, max_habitaciones))

                if precio_max != '':
                    values_list.append((0, precio_max))

                operator = 'and'

                inmuebles_list = dynamic_query(Inmueble, fields_list, types_list, values_list, operator).distinct()

                # Eliminando repetidos
                # if orden == 'precio' or orden == 'metros':
                #     for inmueble in inmuebles_list:
                #         modulos = Modulo.objects.filter(inmueble=inmueble)
                #         if inmueble not in inmuebles:
                #             if modulos:
                #                 inmuebles.append(inmueble)
                #             else:
                #                 inmuebles.insert(0, inmueble)
                #     inmuebles_list = inmuebles
    else:
        pais = Pais.objects.get(nombre=pais)

    # Verificacion de cual de los filtros se uso
    if inmuebles_inf != 24 and inmuebles_inf != '':
        inmuebles_pagina = inmuebles_inf
    if inmuebles_sup != 24 and inmuebles_sup != '':
        inmuebles_pagina = inmuebles_sup

    # Busqueda de propiedades en el pais actual
    paginator = Paginator(inmuebles_list, inmuebles_pagina)
    page = request.GET.get('page')

    # Busqueda con paginacion
    query = request.GET.copy()
    if 'page' in query:
        del query['page']
    try:
        inmuebles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        inmuebles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        inmuebles = paginator.page(paginator.num_pages)

    buscadorF.fields['ciudad'] = forms.ModelChoiceField(Ciudad.objects.filter(pais__nombre=pais), empty_label=' - Ciudad -')
    buscadorF.fields['zona'] = forms.ModelChoiceField(Zona.objects.filter(ciudad__pais__nombre=pais), empty_label=' - Zona -')

    for pais in Pais.objects.filter(nombre=pais):
        ciudades[pais.id] = dict(Ciudad.objects.filter(pais=pais).values_list('id', 'nombre'))
    ciudades = json.dumps(ciudades)

    for ciudad in Ciudad.objects.filter(pais__nombre=pais):
        zonas[ciudad.id] = dict(Zona.objects.filter(ciudad=ciudad).values_list('id', 'nombre'))
    zonas = json.dumps(zonas)

    # Banners publicitarios de cada pais
    banners = Banner.objects.filter(pais__nombre=pais).order_by('nombre')

    ctx = {
        'buscadorF': buscadorF,
        'moneda_get': moneda_get,
        'moneda': moneda,
        'pais': pais,
        'inmuebles': inmuebles,
        'inmuebles_pagina': inmuebles_pagina,
        'imagen_banner': imagen_banner,
        'ciudades': ciudades,
        'zonas': zonas,
        'banners': banners,
        'query': query,
    }

    return render_to_response('home/home.html', ctx, context_instance=RequestContext(request))


# Vista de cada inmueble
def inmueble(request, codigo, pais):

    constructor = False
    visita = False
    financiamiento = False
    envio_contacto = False
    envio_visita = False
    envio_financiamiento = False
    fecha_entrega = ''
    modulos_favs = []
    user = request.user

    # Inmueble
    inmueble = get_object_or_404(Inmueble, codigo=codigo, pais__nombre=pais)

    # Modulos
    modulos = Modulo.objects.filter(inmueble=inmueble).order_by('metros')

    try:
        modulos_favs = ModuloFavorito.objects.filter(usuario=user, modulo__in=modulos).values_list('modulo', flat=True)
    except:
        modulos_favs = []

    # Agente
    agente = inmueble.agente
    telefonos = TelefonoAgente.objects.filter(agente=agente)

    # Contacto con el agente
    contactoF = ContactoAgenteForm()

    # Solicitar visita al inmueble
    solicitarvF = SolicitarVisitaForm()

    # Solicitar financiamiento
    financiamientoF = SolicitarFinanciamientoForm()

    # Imagenes del inmueble
    imagenes = ImagenInmueble.objects.filter(inmueble=inmueble).order_by('id')

    fecha_entrega = inmueble.fecha_entrega[:2] + inmueble.fecha_entrega[5:]
    fecha_entrega = datetime.strptime(fecha_entrega, "%m/%Y")

    # Moneda
    try:
        moneda = Moneda.objects.get(pais__nombre=pais)
    except:
        moneda = ''

    # Banners del home
    banners = Banner.objects.filter(pais__nombre=pais)

    # Vista del inmueble por parte del usuario
    visto = inmueble_vista_count(request, inmueble.id)

    if not visto:
        # Crear una vista nueva o actualizar la cantidad
        try:
            vista = InmuebleView.objects.get(inmueble=inmueble)
            vista.cantidad += 1
            vista.save()
        except:
            vista = InmuebleView(cantidad=1, inmueble=inmueble)
            vista.save()

    if request.POST:
        if 'constructor' in request.POST:
            constructor = True
            contactoF = ContactoAgenteForm(request.POST)

            if contactoF.is_valid():
                envio_contacto = contact_email(request, contactoF, agente.correo, inmueble)
                financiamientoF = SolicitarFinanciamientoForm()
                solicitarvF = SolicitarVisitaForm()

        elif 'visita' in request.POST:
            visita = True
            solicitarvF = SolicitarVisitaForm(request.POST)

            if solicitarvF.is_valid():
                envio_visita = visit_email(request, solicitarvF, inmueble)
                financiamientoF = SolicitarFinanciamientoForm()
                contactoF = ContactoAgenteForm()

        elif 'financiamiento' in request.POST:
            financiamiento = True
            financiamientoF = SolicitarFinanciamientoForm(request.POST)

            if financiamientoF.is_valid():
                envio_financiamiento = financiamiento_email(request, pais, financiamientoF, inmueble)
                solicitarvF = SolicitarVisitaForm()
                contactoF = ContactoAgenteForm()

    ctx = {
        'inmueble': inmueble,
        'modulos': modulos,
        'modulos_favs': modulos_favs,
        'moneda': moneda,
        'telefonosAgente': telefonos,
        'ContactoAgenteForm': contactoF,
        'SolicitarVisitaForm': solicitarvF,
        'SolicitarFinanciamientoForm': financiamientoF,
        'imagenes': imagenes,
        'banners': banners,
        'pais': pais,
        'constructor': constructor,
        'envio_contacto': envio_contacto,
        'visita': visita,
        'financiamiento': financiamiento,
        'envio_visita': envio_visita,
        'envio_financiamiento': envio_financiamiento,
        'fecha_entrega': fecha_entrega,
    }

    return render_to_response('inmuebles/inmueble.html', ctx, context_instance=RequestContext(request))


# Vista para enviar reporte de mercado de usuarios
def inmueble_reporte_mercado(request, pais, id_inmueble):

    user = request.user
    url = '/' + str(pais) + '/favoritos/'

    inmueble = []
    try:
        inmueble = Inmueble.objects.get(id=id_inmueble)
    except:
        inmueble = None

    reporte_email(request, user, pais, inmueble)

    return HttpResponseRedirect(url)


# Vista de inmuebles favoritos
def favoritos_list(request, pais):

    inmuebles = []
    modulos = []
    user = request.user

    if user.is_authenticated() and request.user:

        # Moneda
        try:
            moneda = Moneda.objects.get(pais__nombre=pais)
        except:
            moneda = ''

        inmuebles = InmuebleFavorito.objects.filter(usuario=request.user).order_by('inmueble__pais__nombre')
        modulos = ModuloFavorito.objects.filter(usuario=request.user).order_by('modulo__inmueble__pais__nombre')
    else:
        return HttpResponseRedirect('/' + str(pais) + '/ingreso-registro/')

    ctx = {
        'moneda': moneda,
        'pais': pais,
        'inmueblesFavoritos': inmuebles,
        'modulosFavoritos': modulos
    }

    return render_to_response('favoritos/listar.html', ctx, context_instance=RequestContext(request))


# Vista para agregar inmuebles favoritos
def favoritos_agregar(request, pais, id_inmueble):

    user = request.user
    url = '/'

    if user.is_authenticated() and request.user:
        try:
            inmueble = InmuebleFavorito.objects.get(inmueble__id=id_inmueble, usuario=user)
        except:
            url = '/' + str(pais) + '/favoritos/'

        if inmueble:
            favorito = InmuebleFavorito(inmueble=inmueble, usuario=user)
            favorito.save()
            url = '/' + str(pais) + '/favoritos/'
    else:
        url = '/' + str(pais) + '/ingreso-registro/'
        return HttpResponseRedirect(url)


# Vista para eliminar inmuebles favoritos
def favoritos_eliminar(request, pais, id_inmueble):
    user = request.user
    url = '/'

    if user.is_authenticated() and request.user:
        try:
            inmueble = InmuebleFavorito.objects.get(inmueble__id=id_inmueble, usuario=user)
            inmueble.delete()
        except:
            url = '/'

        url = '/' + str(pais) + '/favoritos/'
    else:
        url = '/' + str(pais) + '/ingreso-registro/'

    return HttpResponseRedirect(url)


# Vista para agregar modulos de inmuebles favoritos
def favoritos_modulo_agregar(request, pais, id_modulo):

    modulo = Modulo.objects.get(id=id_modulo)
    moduloF = None
    user = request.user
    url = '/'

    if user.is_authenticated() and user:
        try:
            moduloF = ModuloFavorito.objects.get(modulo__id=id_modulo, usuario=user)
        except:
            url = '/' + str(pais) + '/favoritos/'

        if not moduloF:
            favorito = ModuloFavorito(modulo_id=id_modulo, usuario=user)
            favorito.save()
            url = '/' + str(pais) + '/inmuebles/' + str(modulo.inmueble.codigo) + '/'
    else:
        url = '/' + str(pais) + '/ingreso-registro/'

    return HttpResponseRedirect(url)


# Vista para eliminar inmuebles favoritos
def favoritos_modulo_eliminar(request, pais, id_modulo):

    modulo = None
    user = request.user
    url = '/'

    if user.is_authenticated() and user:
        try:
            modulo = ModuloFavorito.objects.get(modulo__id=id_modulo, usuario=user)
            modulo.delete()
        except:
            url = '/'

        url = '/' + str(pais) + '/favoritos/'
    else:
        url = '/' + str(pais) + '/ingreso-registro/'

    return HttpResponseRedirect(url)


# Vista para enviar los favoritos al usuario
def favoritos_enviar(request, pais):

    return_val = True
    user = request.user
    favoritos = []
    url = '/' + str(pais) + '/favoritos/'

    try:
        favoritos = ModuloFavorito.objects.filter(usuario=user)
    except:
        return_val = False

    if return_val:
        return_val = favoritos_email(request, user, favoritos, pais)

    return HttpResponseRedirect(url)


# Vista para generar pdfs
class FavoritosPdfList(PDFTemplateView):
    template_name = "favoritos/pdf_template.html"

    def get_context_data(self, **kwargs):
        moneda = ''

        context = super(FavoritosPdfList, self).get_context_data(**kwargs)

        modulos = ModuloFavorito.objects.filter(usuario=self.request.user).order_by('modulo__inmueble__pais__nombre')
        context['modulosFavoritos'] = modulos

        # Moneda
        try:
            moneda = Moneda.objects.get(pais__nombre=context['pais'])
        except:
            moneda = ''

        context['moneda'] = moneda

        return context


# Vista para contar las vistas de un inmueble por los diferentes usuarios
def inmueble_vista_count(request, id_inmueble):
    visto = False

    if not request.user.is_superuser:
        if request.session.get('vistas'):
            inmuebles = request.session['vistas']
            if int(id_inmueble) not in inmuebles:
                inmuebles.append(int(id_inmueble))
                request.session['vistas'] = inmuebles
            else:
                visto = True
        else:
            request.session['vistas'] = [int(id_inmueble)]
    else:
        visto = True

    return visto


# Vista para contar los clicks de los usuarios a los links de los agentes
def inmueble_link_agente(request, pais, id_inmueble):

    inmueble = Inmueble.objects.get(codigo=id_inmueble)
    click = inmueble_click_count(request, id_inmueble)

    if not click:
        try:
            click = InmuebleConstructorClick.objects.get(inmueble=inmueble)
            click.cantidad += 1
            click.save()
        except:
            click = InmuebleConstructorClick(cantidad=1, agente=inmueble.agente, inmueble=inmueble)
            click.save()

    return HttpResponseRedirect('http://' + inmueble.agente.pagina)


# Vista para contar los clicks de los usuarios a los links de skype los agentes
def inmueble_call_agente(request, pais, id_inmueble):

    inmueble = Inmueble.objects.get(codigo=id_inmueble)

    try:
        click = InmuebleSkypeClick.objects.get(inmueble=inmueble)
        click.cantidad += 1
        click.save()
    except:
        click = InmuebleSkypeClick(cantidad=1, agente=inmueble.agente, inmueble=inmueble)
        click.save()

    return HttpResponseRedirect('/' + str(pais) + '/inmuebles/' + str(id_inmueble))


# Vista para contar los clicks de los usuarios a los links de los agentes
def inmueble_click_count(request, id_inmueble):
    clickeo = False

    if request.session.get('clicks'):
        inmuebles = request.session['clicks']
        if int(id_inmueble) not in inmuebles:
            inmuebles.append(int(id_inmueble))
            request.session['clicks'] = inmuebles
        else:
            clickeo = True
    else:
        request.session['clicks'] = [int(id_inmueble)]

    return clickeo


# Vista para contar los clicks de los usuarios a los links de skype de agentes
def inmueble_click_skype_count(request, id_inmueble):
    clickeo = False

    if request.session.get('skype'):
        inmuebles = request.session['skype']
        if int(id_inmueble) not in inmuebles:
            inmuebles.append(int(id_inmueble))
            request.session['skype'] = inmuebles
        else:
            clickeo = True
    else:
        request.session['skype'] = [int(id_inmueble)]

    return clickeo


# Vista para el ingreso y registro de los usuarios.
def login_register_user(request, pais):

    username = ''
    password = ''
    usuario = ''
    error_login = ''
    registrado = False

    # Formularios basicos
    loginF = LoginForm()
    registroF = UserForm()

    # Formulario para los paises disponibles
    paisesF = PaisesForm(initial={
        'pais': pais,
    })

    if request.user.is_authenticated() and request.user:
        return HttpResponseRedirect('/' + str(pais) + '/perfil/')

    if request.POST:
        if 'registro' in request.POST:
            registroF = UserForm(request.POST)

            if registroF.is_valid():
                registroF.save()
                registrado = True
        elif 'login' in request.POST:
            loginF = LoginForm(request.POST)

            if loginF.is_valid():
                try:
                    username = request.POST['user_name']
                    password = request.POST['password']
                    usuario = authenticate(username=username, password=password)
                except:
                    print 'Error Validating User'

                if usuario:
                    # Caso del usuario activo
                    if usuario.is_active:
                        login(request, usuario)
                        return HttpResponseRedirect('/' + str(pais) + '/favoritos/')
                    else:
                        return "Tu cuenta esta bloqueada"
                else:
                    # Usuario invalido o no existe!
                    print "Invalid login details: {0}, {1}".format(username, password)
                    error_login = '¡Contraseña invalida!'

    ctx = {
        'registrado': registrado,
        'pais': pais,
        'login': loginF,
        'registro': registroF,
        'paisesF': paisesF,
        'error_login': error_login,
    }

    return render_to_response('usuarios/login-registro.html', ctx, context_instance=RequestContext(request))


# Vista para el perfil de usuarios comunes.
@login_required
def perfil_user(request, pais):

    # Formulario para los paises disponibles
    paisesF = PaisesForm(initial={
        'pais': pais,
    })

    ctx = {
        'pais': pais,
        'paisesF': paisesF,
    }
    return render_to_response('usuarios/perfil.html', ctx, context_instance=RequestContext(request))


# Vista para editar el perfil de usuarios comunes.
@login_required
def perfil_editar_user(request, pais):
    exito = False
    user = request.user

    # Formulario para los paises disponibles
    paisesF = PaisesForm(initial={
        'pais': pais,
    })

    userF = EditUserForm(instance=user)

    if(request.POST):
        userF = EditUserForm(request.POST, instance=user)

        if userF.is_valid():
            userF.save()
            exito = True

    ctx = {
        'pais': pais,
        'paisesF': paisesF,
        'userF': userF,
        'exito': exito,
    }
    return render_to_response('usuarios/editar.html', ctx, context_instance=RequestContext(request))


# Vista para cerrar la sesion de usuario comun
@login_required
def perfil_logout(request, pais):

    logout(request)
    return HttpResponseRedirect('/' + str(pais) + '/')


# Vista para el ingreso de los usuarios administradores.
def login_admin(request, pais):

    username = ''
    password = ''
    buscadorF = BuscadorForm()
    buscadorF.fields['ciudad'] = forms.ModelChoiceField(Ciudad.objects.filter(pais__nombre=pais), empty_label=' - Ciudad -')
    buscadorF.fields['zona'] = forms.ModelChoiceField(Zona.objects.filter(ciudad__pais__nombre=pais), empty_label=' - Zona -')

    # Formularios basicos
    loginF = LoginForm()

    if request.user.is_authenticated() and request.user:
        return HttpResponseRedirect('/' + str(pais) + '/admin/perfil/')

    if request.method == "POST":
        loginF = LoginForm(request.POST)
        username = request.POST['user_name']
        password = request.POST['password']
        usuario = authenticate(username=username, password=password)

        if usuario:
                # Caso del usuario activo
                if usuario.is_active:
                    login(request, usuario)
                    return HttpResponseRedirect('/' + str(pais) + '/admin/perfil/')
                else:
                    return "Tu cuenta esta bloqueada"
        else:
            # Usuario invalido o no existe!
            print "Invalid login details: {0}, {1}".format(username, password)

    ctx = {
        'pais': pais,
        'login': loginF,
        'buscadorF': buscadorF,
    }

    return render_to_response('login/login.html', ctx, context_instance=RequestContext(request))


# Vista para el perfil de usuarios del admin
@login_required
def perfil_admin(request, pais):

    inmuebles = Inmueble.objects.filter(pais__nombre=pais)
    try:
        agentes = Agente.objects.filter(pais__nombre=pais)
    except:
        agentes = Agente.objects.all()

    ciudades = Ciudad.objects.filter(pais__nombre=pais)
    zonas = Zona.objects.filter(ciudad__pais__nombre=pais)

    nombre_pais = dict(countries)[pais]

    ctx = {
        'inmuebles': inmuebles,
        'agentes': agentes,
        'ciudades': ciudades,
        'zonas': zonas,
        'pais': pais,
        'nombre_pais': nombre_pais,
    }
    return render_to_response('admin/perfil.html', ctx, context_instance=RequestContext(request))


# Vista para listar los inmuebles de ese pais
@login_required
def inmuebles_list(request, pais):
    inmuebles = Inmueble.objects.filter(pais__nombre=pais).order_by('titulo')
    nombre_pais = dict(countries)[pais]

    ctx = {
        'inmuebles': inmuebles,
        'pais': pais,
        'nombre_pais': nombre_pais,
    }

    return render_to_response('admin/inmuebles/inmuebles.html', ctx, context_instance=RequestContext(request))


# Vista para elegir el tipo de inmueble a publicar
class ElegirTipo(TemplateView):

    template_name = "admin/inmuebles/elegir-tipo.html"

    def get_context_data(self, **kwargs):
        context = super(ElegirTipo, self).get_context_data(**kwargs)
        tipos = BuscadorForm()
        context['pais'] = kwargs['pais']
        context['tipos'] = tipos
        return context


# Vista para elegir el tipo de inmueble a publicar
class DetalleInmueble(TemplateView):

    template_name = "admin/inmuebles/detalle.html"

    def get_context_data(self, **kwargs):
        context = super(DetalleInmueble, self).get_context_data(**kwargs)
        context['inmueble'] = get_object_or_404(Inmueble, id=kwargs['id_inmueble'])
        context['modulos'] = Modulo.objects.filter(inmueble=context['inmueble'])
        try:
            context['vistas'] = InmuebleView.objects.get(inmueble=context['inmueble'])
        except:
            context['vistas'] = ''

        try:
            context['clicks'] = InmuebleConstructorClick.objects.get(inmueble=context['inmueble'])
        except:
            context['clicks'] = ''

        try:
            context['skype'] = InmuebleSkypeClick.objects.get(inmueble=context['inmueble'])[:1]
        except:
            context['skype'] = ''

        context['pais'] = kwargs['pais']
        return context


# Vista para publicar el inmueble
class Publicar(CreateView):
    template_name = 'admin/inmuebles/publicar.html'
    model = Inmueble
    form = InmuebleForm
    widgets = {
        'latitud': forms.HiddenInput(),
        'longitud': forms.HiddenInput(),
    }

    fields = ['titulo',
              'codigo',
              'descripcion',
              'ciudad',
              'zona',
              'direccion',
              'pagina',
              'video',
              'fecha_entrega',
              'tipo_obra',
              'agente',
              'latitud',
              'longitud',
              'areas_comunes',
              'logo',
              'visible',
              'archivo',
              'ficha_tecnica',
              'forma_pago']

    def get(self, request, *args, **kwargs):
        self.object = None
        zonas = {}
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.fields['agente'] = forms.ModelChoiceField(Agente.objects.filter(pais__nombre=kwargs["pais"]))
        form.fields['ciudad'] = forms.ModelChoiceField(Ciudad.objects.filter(pais__nombre=kwargs["pais"]))
        form.fields['zona'] = forms.ModelChoiceField(Zona.objects.filter(ciudad__pais__nombre=kwargs["pais"]))
        tipo = get_object_or_404(TipoInmueble, id=kwargs["tipo"])
        campos = CampoTipoInmueble.objects.filter(tipo_inmueble=tipo)

        for ciudad in Ciudad.objects.filter(pais__nombre=kwargs["pais"]):
            zonas[ciudad.id] = dict(Zona.objects.filter(ciudad=ciudad).values_list('id', 'nombre'))
        zonas = json.dumps(zonas)

        ValorCampoTipoInmuebleFormset = inlineformset_factory(Inmueble,
                                                              ValorCampoTipoInmueble,
                                                              extra=campos.count(),
                                                              can_delete=False,
                                                              min_num=campos.count(),
                                                              max_num=campos.count(),
                                                              fields=['campo', 'valor'])
        return self.render_to_response(self.get_context_data(form=form, pais=kwargs["pais"], zonas=zonas))

    def post(self, request, *args, **kwargs):
        self.object = None
        zonas = {}
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.fields['agente'] = forms.ModelChoiceField(Agente.objects.filter(pais__nombre=kwargs["pais"]))
        form.fields['ciudad'] = forms.ModelChoiceField(Ciudad.objects.filter(pais__nombre=kwargs["pais"]))
        form.fields['zona'] = forms.ModelChoiceField(Zona.objects.filter(ciudad__pais__nombre=kwargs["pais"]))
        tipo = get_object_or_404(TipoInmueble, id=kwargs["tipo"])
        campos = CampoTipoInmueble.objects.filter(tipo_inmueble=tipo)
        for ciudad in Ciudad.objects.filter(pais__nombre=kwargs["pais"]):
            zonas[ciudad.id] = dict(Zona.objects.filter(ciudad=ciudad).values_list('id', 'nombre'))
        zonas = json.dumps(zonas)

        ValorCampoTipoInmuebleFormset = inlineformset_factory(Inmueble,
                                                              ValorCampoTipoInmueble,
                                                              extra=campos.count(),
                                                              min_num=campos.count(),
                                                              max_num=campos.count(),
                                                              can_delete=False,
                                                              fields=['campo', 'valor'])

        if form.is_valid():
            return self.form_valid(form, tipo, kwargs["pais"])
        else:
            return self.form_invalid(form, zonas, kwargs["pais"])

    def form_valid(self, form, tipo, pais):
        self.object = form.save(commit=False)
        self.object.pais = Pais.objects.get(nombre=pais)
        self.object.tipo = tipo
        self.object.fecha_expiracion = datetime.now()
        self.object.save()
        return redirect('inmuebles:listar_inmuebles', pais=pais)

    def form_invalid(self, form, zonas, pais):
        return self.render_to_response(
            self.get_context_data(form=form, pais=pais, zonas=zonas))


# Vista para publicar el inmueble
class AgregarModulo(CreateView):
    template_name = 'admin/inmuebles/agregar-modulo.html'
    model = Modulo
    fields = ['tipo',
              'metros',
              'banos',
              'dormitorios',
              'estacionamientos',
              'precio',
              'plano']

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        inm = get_object_or_404(Inmueble, id=kwargs['id_inmueble'])
        return self.render_to_response(self.get_context_data(form=form,
                                                             inmueble=inm,
                                                             pais=kwargs["pais"]))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form, kwargs["pais"], kwargs["id_inmueble"])
        else:
            return self.form_invalid(form, kwargs["pais"], kwargs["id_inmueble"])

    def form_valid(self, form, pais, id_inmueble):
        self.object = form.save(commit=False)
        tasa = Moneda.objects.get(pais__nombre=pais)
        self.object.precio = int(self.object.precio)
        self.object.inmueble = Inmueble.objects.get(id=id_inmueble)
        self.object.save()
        return redirect('inmuebles:detalle', pais=pais, id_inmueble=id_inmueble)

    def form_invalid(self, form, pais, id_inmueble):
        inm = get_object_or_404(Inmueble, id=id_inmueble)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  inmueble=inm,
                                  pais=pais))


# Vista para publicar el inmueble
class EditarModulo(UpdateView):
    template_name = 'admin/inmuebles/agregar-modulo.html'
    model = Modulo
    pk_url_kwarg = 'id_modulo'
    fields = ['tipo',
              'metros',
              'banos',
              'dormitorios',
              'estacionamientos',
              'precio',
              'plano']

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        tasa = Moneda.objects.get(pais__nombre=kwargs["pais"])
        self.object.precio = self.object.precio
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        inm = get_object_or_404(Inmueble, id=kwargs['id_inmueble'])
        return self.render_to_response(self.get_context_data(form=form,
                                                             inmueble=inm,
                                                             pais=kwargs["pais"]))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form, kwargs["pais"], kwargs["id_inmueble"])
        else:
            return self.form_invalid(form, kwargs["pais"], kwargs["id_inmueble"])

    def form_valid(self, form, pais, id_inmueble):
        tasa = Moneda.objects.get(pais__nombre=pais)
        self.object.precio = int(self.object.precio)
        self.object.inmueble = Inmueble.objects.get(id=id_inmueble)
        self.object.save()
        return redirect('inmuebles:detalle', pais=pais, id_inmueble=id_inmueble)

    def form_invalid(self, form, pais, id_inmueble):
        inm = get_object_or_404(Inmueble, id=id_inmueble)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  inmueble=inm,
                                  pais=pais))


# Vista para eliminar los modulos
@login_required
def modulos_eliminar(request, pais, id_inmueble, id_modulo):
    get_object_or_404(Modulo, id=id_modulo).delete()

    return redirect('inmuebles:detalle', pais=pais, id_inmueble=id_inmueble)


# Vista para editar los inmuebles
@login_required
def inmuebles_editar(request, pais, id_inmueble):

    editado = ''
    inmueble = Inmueble.objects.get(id=id_inmueble)
    inmuebleF = InmuebleForm(instance=inmueble)
    inmuebleF.fields['agente'] = forms.ModelChoiceField(Agente.objects.filter(pais__nombre=pais))
    inmuebleF.fields['ciudad'] = forms.ModelChoiceField(Ciudad.objects.filter(pais__nombre=pais))
    inmuebleF.fields['zona'] = forms.ModelChoiceField(Zona.objects.filter(ciudad__pais__nombre=pais))
    tiposF = BuscadorForm(initial={'tipo': inmueble.tipo})

    if request.POST:
        inmuebleF = InmuebleForm(request.POST, request.FILES, instance=inmueble)
        tiposF = BuscadorForm(request.POST)

        if inmuebleF.is_valid() and tiposF.is_valid():
            tipo = tiposF.cleaned_data['tipo']
            inmueble = inmuebleF.save(commit=False)
            inmueble.tipo = tipo
            inmuebleF.save()
            editado = True

    ctx = {
        'InmuebleForm': inmuebleF,
        'TiposForm': tiposF,
        'editado': editado,
        'pais': pais,
    }

    return render_to_response('admin/inmuebles/editar.html', ctx, context_instance=RequestContext(request))


# Vista para agregar las imagenes del inmueble
def inmuebles_imagenes(request, pais, id_inmueble):

    editado = ''
    inmueble = Inmueble.objects.get(id=id_inmueble)
    thumb = ThumbInmueble.objects.filter(inmueble=inmueble)
    imagenes = ImagenInmueble.objects.filter(inmueble=inmueble)

    # Formset de imagen
    ImagenFormset = inlineformset_factory(Inmueble, ImagenInmueble, form = ImagenInmuebleForm, can_delete=True, extra=1, max_num=len(imagenes) + 2, fields=['imagen', 'descripcion'])
    inmuebleF = ImagenFormset(instance=inmueble, queryset=ImagenInmueble.objects.filter(inmueble=inmueble))

    # Form del thumbnail del inmueble
    if thumb:
        thumbF = ThumbInmuebleForm(instance=thumb[0])
    else:
        thumbF = ThumbInmuebleForm()

    if request.POST:
        inmuebleF = ImagenFormset(request.POST, request.FILES, instance=inmueble)
        if inmuebleF.is_valid():
            inmuebleF.save()

    inmuebleF = ImagenFormset(instance=inmueble, queryset=ImagenInmueble.objects.filter(inmueble=inmueble))

    ctx = {
        'ThumbForm': thumbF,
        'InmuebleForm': inmuebleF,
        'id_inmueble': id_inmueble,
        'editado': editado,
        'pais': pais,
    }

    return render_to_response('admin/inmuebles/imagenes-inmueble.html', ctx, context_instance=RequestContext(request))


# Vista para agregar las imagenes del inmueble
def inmuebles_thumbnail(request, pais, id_inmueble):
    inmueble = Inmueble.objects.get(id=id_inmueble)
    thumb = ThumbInmueble.objects.filter(inmueble=inmueble)

    if request.POST:
        if thumb:
            thumbF = ThumbInmuebleForm(request.POST, request.FILES, instance=thumb[0])
        else:
            thumbF = ThumbInmuebleForm(request.POST, request.FILES)

        if thumbF.is_valid():
            thumb_new = thumbF.save(commit=False)
            thumb_new.principal = False
            thumb_new.inmueble = inmueble
            thumbF.save()

    return HttpResponseRedirect('/' + str(pais) + '/admin/inmuebles/imagenes/' + id_inmueble + '/')


# Vista para agregar los agentes de ese pais
@login_required
def inmuebles_eliminar(request, pais, id_inmueble):

    get_object_or_404(Inmueble, id=id_inmueble).delete()
    return HttpResponseRedirect('/' + str(pais) + '/admin/inmuebles/')


# Vista para listar los agentes de ese pais
@login_required
def agentes_list(request, pais):

    agentes = Agente.objects.filter(pais__nombre=pais)
    nombre_pais = dict(countries)[pais]

    ctx = {
        'agentes': agentes,
        'pais': pais,
        'nombre_pais': nombre_pais,
    }

    return render_to_response('admin/agentes/agentes.html', ctx, context_instance=RequestContext(request))


# Vista para agregar los agentes de ese pais
@login_required
def agentes_agregar(request, pais):

    agenteF = AgenteForm()
    telefonoFormSet = inlineformset_factory(Agente, TelefonoAgente, extra=6, max_num=6, form=TelefonoAgenteForm, can_delete=True)
    telefonoAgenteF = telefonoFormSet()

    if request.POST:
        agenteF = AgenteForm(request.POST, request.FILES)
        telefonoFormSet = inlineformset_factory(Agente, TelefonoAgente, extra=6, max_num=6, form=TelefonoAgenteForm, can_delete=True)
        telefonoAgenteF = telefonoFormSet(request.POST)

        if agenteF.is_valid() and telefonoAgenteF.is_valid():
            agente = agenteF.save(commit=False)
            pais = Pais.objects.get(nombre=pais)
            agente.pais = pais
            agente.save()

            # Verificacion de telefonos del agente
            for form in telefonoAgenteF:

                # Verificar que se llenaron los numeros
                try:
                    numero = form.cleaned_data['numero']
                except:
                    numero = ''

                if numero != '':
                    telefono = form.save(commit=False)
                    telefono.agente = agente
                    telefono.save()

            return HttpResponseRedirect('/' + str(pais) + '/admin/agentes/')

    ctx = {
        'TelefonoAgenteForm': telefonoAgenteF,
        'AgenteForm': agenteF,
        'pais': pais,
    }

    return render_to_response('admin/agentes/agregar.html', ctx, context_instance=RequestContext(request))


# Vista para agregar los agentes de ese pais
@login_required
def agentes_editar(request, pais, id_agente):

    editado = ''
    agente = Agente.objects.get(id=id_agente)
    agenteF = AgenteForm(instance=agente)
    telefonoFormSet = inlineformset_factory(Agente, TelefonoAgente, extra=6, max_num=6, form=TelefonoAgenteForm, can_delete=True)
    telefonoAgenteF = telefonoFormSet(instance=agente)

    if request.POST:
        agenteF = AgenteForm(request.POST, request.FILES, instance=agente)
        telefonoFormSet = inlineformset_factory(Agente, TelefonoAgente, extra=6, max_num=6, form=TelefonoAgenteForm, can_delete=True)
        telefonoAgenteF = telefonoFormSet(request.POST, instance=agente)
        if agenteF.is_valid() and telefonoAgenteF.is_valid():
            agenteF.save()
            telefonoAgenteF.save()
            editado = True

    telefonoFormSet = inlineformset_factory(Agente, TelefonoAgente, extra=6, max_num=6, form=TelefonoAgenteForm, can_delete=True)
    telefonoAgenteF = telefonoFormSet(instance=agente)

    ctx = {
        'AgenteForm': agenteF,
        'TelefonoAgenteForm': telefonoAgenteF,
        'editado': editado,
        'pais': pais,
    }

    return render_to_response('admin/agentes/editar.html', ctx, context_instance=RequestContext(request))


# Vista para agregar los agentes de ese pais
@login_required
def agentes_eliminar(request, pais, id_agente):

    get_object_or_404(Agente, id=id_agente).delete()

    return HttpResponseRedirect('/' + str(pais) + '/admin/agentes/')


# Vista para listar las ciudades de ese pais
@login_required
def ciudades_list(request, pais):

    ciudades = Ciudad.objects.filter(pais__nombre=pais)
    nombre_pais = dict(countries)[pais]

    ctx = {
        'ciudades': ciudades,
        'pais': pais,
        'nombre_pais': nombre_pais,
    }

    return render_to_response('admin/ciudades/ciudades.html', ctx, context_instance=RequestContext(request))


# Vista para agregar las ciudades de ese pais
@login_required
def ciudades_agregar(request, pais):

    ciudadF = CiudadForm()

    if request.POST:
        ciudadF = CiudadForm(request.POST)
        if ciudadF.is_valid():
            ciudad = ciudadF.save(commit=False)
            pais = Pais.objects.get(nombre=pais)
            ciudad.pais = pais
            ciudad.save()

            return HttpResponseRedirect('/' + str(pais) + '/admin/ciudades/')

    ctx = {
        'CiudadForm': ciudadF,
        'pais': pais,
    }

    return render_to_response('admin/ciudades/agregar.html', ctx, context_instance=RequestContext(request))


# Vista para agregar las ciudades de ese pais
@login_required
def ciudades_editar(request, pais, id_ciudad):

    editado = ''
    ciudad = Ciudad.objects.get(id=id_ciudad)
    ciudadF = CiudadForm(instance=ciudad)

    if request.POST:
        ciudadF = CiudadForm(request.POST, instance=ciudad)
        if ciudadF.is_valid():
            ciudadF.save()
            editado = True

    ctx = {
        'CiudadForm': ciudadF,
        'editado': editado,
        'pais': pais,
    }

    return render_to_response('admin/ciudades/editar.html', ctx, context_instance=RequestContext(request))


# Vista para agregar los agentes de ese pais
@login_required
def ciudades_eliminar(request, pais, id_ciudad):

    get_object_or_404(Ciudad, id=id_ciudad).delete()

    return HttpResponseRedirect('/' + str(pais) + '/admin/ciudades/')


# Vista para listar las ciudades de ese pais
@login_required
def zonas_list(request, pais):

    zonas = Zona.objects.filter(ciudad__pais__nombre=pais)
    nombre_pais = dict(countries)[pais]

    ctx = {
        'zonas': zonas,
        'pais': pais,
        'nombre_pais': nombre_pais,
    }

    return render_to_response('admin/zonas/zonas.html', ctx, context_instance=RequestContext(request))


# Vista para agregar las ciudades de ese pais
@login_required
def zonas_agregar(request, pais):

    zonaF = ZonaForm()

    if request.POST:
        zonaF = ZonaForm(request.POST)
        if zonaF.is_valid():
            zonaF.save()

            return HttpResponseRedirect('/' + str(pais) + '/admin/zonas/')

    zonaF.fields['ciudad'] = forms.ModelChoiceField(Ciudad.objects.filter(pais__nombre=pais), empty_label=' - Ciudad -')

    ctx = {
        'ZonaForm': zonaF,
        'pais': pais,
    }

    return render_to_response('admin/zonas/agregar.html', ctx, context_instance=RequestContext(request))


# Vista para agregar las ciudades de ese pais
@login_required
def zonas_editar(request, pais, id_zona):

    editado = ''
    zona = Zona.objects.get(id=id_zona)
    zonaF = ZonaForm(instance=zona)

    if request.POST:
        zonaF = ZonaForm(request.POST, instance=zona)
        if zonaF.is_valid():
            zonaF.save()
            editado = True

    zonaF.fields['ciudad'] = forms.ModelChoiceField(Ciudad.objects.filter(pais__nombre=pais), empty_label=' - Ciudad -')

    ctx = {
        'ZonaForm': zonaF,
        'editado': editado,
        'pais': pais,
    }

    return render_to_response('admin/zonas/editar.html', ctx, context_instance=RequestContext(request))


# Vista para agregar los agentes de ese pais
@login_required
def zonas_eliminar(request, pais, id_zona):

    get_object_or_404(Zona, id=id_zona).delete()

    return HttpResponseRedirect('/' + str(pais) + '/admin/zonas/')


# Vista para listar las ciudades de ese pais
@login_required
def monedas_list(request, pais):

    try:
        moneda = Moneda.objects.get(pais__nombre=pais)
    except:
        moneda = ''

    nombre_pais = dict(countries)[pais]

    ctx = {
        'moneda': moneda,
        'pais': pais,
        'nombre_pais': nombre_pais,
    }

    return render_to_response('admin/monedas/monedas.html', ctx, context_instance=RequestContext(request))


# Vista para agregar las ciudades de ese pais
@login_required
def monedas_agregar(request, pais):

    monedaF = MonedaForm()

    if request.POST:
        monedaF = MonedaForm(request.POST)
        if monedaF.is_valid():
            moneda = monedaF.save(commit=False)
            pais = Pais.objects.get(nombre=pais)
            moneda.pais = pais
            moneda.save()

            return HttpResponseRedirect('/' + str(pais) + '/admin/monedas/')

    ctx = {
        'MonedaForm': monedaF,
        'pais': pais,
    }

    return render_to_response('admin/monedas/agregar.html', ctx, context_instance=RequestContext(request))


# Vista para agregar las ciudades de ese pais
@login_required
def monedas_editar(request, pais, id_moneda):

    editado = ''
    moneda = Moneda.objects.get(pais__nombre=pais, id=id_moneda)
    monedaF = MonedaForm(instance=moneda)

    if request.POST:
        monedaF = MonedaForm(request.POST, instance=moneda)
        if monedaF.is_valid():
            monedaF.save()
            editado = True

    ctx = {
        'MonedaForm': monedaF,
        'editado': editado,
        'pais': pais,
    }

    return render_to_response('admin/monedas/editar.html', ctx, context_instance=RequestContext(request))


# Vista para eliminar monedas de un pais
@login_required
def monedas_eliminar(request, pais, id_moneda):

    get_object_or_404(Moneda, id=id_moneda).delete()

    return HttpResponseRedirect('/' + str(pais) + '/admin/monedas/')


# Vista de resumen de estadisticas
@login_required
def estadisticas_list(request, pais):

    vistas_total = 0
    clics_total = 0
    skypes_total = 0
    estadisticas = []
    pais = Pais.objects.get(nombre=pais)
    inmuebles = Inmueble.objects.filter(pais__nombre=pais)

    # Estadisticas de cada inmueble
    for inmueble in inmuebles:
        try:
            vistas = InmuebleView.objects.get(inmueble=inmueble)
        except:
            vistas = []

        try:
            clics = InmuebleConstructorClick.objects.get(inmueble=inmueble)
        except:
            clics = []

        try:
            skypes = InmuebleSkypeClick.objects.get(inmueble=inmueble)
        except:
            skypes = []

        if (vistas != []) or (clics != []) or (skypes != []):
            estadisticas.append((inmueble, clics, skypes, vistas))

            if (vistas != []):
                vistas_total += vistas.cantidad

            if (clics != []):
                clics_total += clics.cantidad

            if (skypes != []):
                skypes_total += skypes.cantidad

    ctx = {
        'estadisticas': estadisticas,
        'clics_total': clics_total,
        'skypes_total': skypes_total,
        'vistas_total': vistas_total,
        'inmuebles': inmuebles,
        'pais': pais,
    }

    return render_to_response('admin/estadisticas/estadisticas_listar.html', ctx, context_instance=RequestContext(request))


# Vista para listar los enlaces comerciales
@login_required
def enlaces_list(request, pais):

    enlaces = EnlaceComercial.objects.all()

    ctx = {
        'enlaces': enlaces,
        'pais': pais,
    }

    return render_to_response('admin/enlaces/enlaces.html', ctx, context_instance=RequestContext(request))


# Vista para agregar los enlaces comerciales
@login_required
def enlaces_agregar(request, pais):

    agregado = False
    enlaceF = EnlaceForm()
    if request.POST:
        enlaceF = EnlaceForm(request.POST)
        if enlaceF.is_valid():
            enlaceF.save()
            agregado = True

    ctx = {
        'EnlaceForm': enlaceF,
        'agregado': agregado,
        'pais': pais,
    }

    return render_to_response('admin/enlaces/agregar.html', ctx, context_instance=RequestContext(request))


# Vista para editar los enlaces comerciales
@login_required
def enlaces_editar(request, pais, id_enlace):

    editado = False
    enlace = EnlaceComercial.objects.get(id=id_enlace)
    enlaceF = EnlaceForm(instance=enlace)

    if request.POST:
        enlaceF = EnlaceForm(request.POST, instance=enlace)
        if enlaceF.is_valid():
            enlaceF.save()
            editado = True

    ctx = {
        'EnlaceForm': enlaceF,
        'editado': editado,
        'pais': pais,
    }

    return render_to_response('admin/enlaces/editar.html', ctx, context_instance=RequestContext(request))


# Vista para eliminar enlaces
@login_required
def enlaces_eliminar(request, pais, id_enlace):

    get_object_or_404(EnlaceComercial, id=id_enlace).delete()

    return HttpResponseRedirect('/' + str(pais) + '/admin/enlaces/')


# Vista para los inmuebles móviles
def inmueble_movil(request, codigo):

    inmueble = get_object_or_404(Inmueble, codigo=codigo)
    imagenes = ImagenInmueble.objects.filter(inmueble=inmueble)
    solicitarvF = SolicitarVisitaForm()

    if request.POST:
        solicitarvF = SolicitarVisitaForm(request.POST)

        if solicitarvF.is_valid():
            print 'Yay!'

    ctx = {
        'inmueble': inmueble,
        'imagenes': imagenes,
        'SolicitarVisitaForm': solicitarvF,
    }

    return render_to_response('inmuebles/inmueble_movil.html', ctx, context_instance=RequestContext(request))


# Vista para cerrar la sesion
@login_required
def logout_admin(request, pais):

    logout(request)
    return HttpResponseRedirect('/' + str(pais) + '/')

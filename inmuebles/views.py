from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import get_template
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
from django.core.mail.message import EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_countries import countries
from django import forms
from django.core.urlresolvers import reverse


# Vista del index o home
def index(request):

    #Formulario para los paises disponibles
    paisesF = PaisesForm()

    ctx = {
        'PaisesForm': paisesF,
    }

    return render_to_response('index/index.html', ctx, context_instance=RequestContext(request))


#Vista del home de cada pais
def home(request, pais):

    #Buscador de inmuebles
    buscadorF = BuscadorForm()
    buscadorF.fields['ciudad'] = forms.ModelChoiceField(Ciudad.objects.filter(pais__nombre=pais), empty_label=' - Ciudad -')
    buscadorF.fields['zona'] = forms.ModelChoiceField(Zona.objects.filter(ciudad__pais__nombre=pais), empty_label=' - Zona -')

    #Formulario para los paises disponibles
    paisesF = PaisesForm(initial={
        'pais': pais,
    })

    #Imagenes del slider
    imagenes = Slide.objects.filter(pais__nombre=pais)

    inmuebles_list = Inmueble.objects.filter(pais__nombre=pais)

    #Moneda nacional
    try:
        moneda = Moneda.objects.get(pais__nombre=pais)
    except:
        moneda = ''

    if request.GET:
        buscadorF = BuscadorForm(request.GET)
        #Caso para el buscador de inmuebles
        if buscadorF.is_valid():
            ciudad = buscadorF.cleaned_data['ciudad']
            zona = buscadorF.cleaned_data['zona']
            tipo = buscadorF.cleaned_data['tipo']
            orden = buscadorF.cleaned_data['orden']
            codigo = buscadorF.cleaned_data['codigo']
            palabra = buscadorF.cleaned_data['palabra']

            #Caso de busqueda por codigo
            if codigo != '':
                inmuebles_list = Inmueble.objects.filter(codigo=codigo)
            elif palabra != '':
                inmuebles_list = Inmueble.objects.filter(titulo__contains=palabra)

            # Caso demas
            elif ciudad != None or zona != None or tipo != None or orden != '':

                #Verificacion de string vacio
                if orden == '':
                    orden = None

                #Campos a buscar
                fields_list = []
                fields_list.append('ciudad')
                fields_list.append('zona')
                fields_list.append('tipo')

                #Comparadores para buscar
                types_list=[]
                types_list.append('nombre__exact')
                types_list.append('nombre__exact')
                types_list.append('nombre__exact')

                #Valores a buscar
                values_list=[]
                values_list.append(ciudad)
                values_list.append(zona)
                values_list.append(tipo)

                operator = 'and'

                inmuebles_list = dynamic_query(Inmueble, fields_list, types_list, values_list, operator, orden)

    #Busqueda de propiedades en el pais actual
    paginator = Paginator(inmuebles_list, 6)
    page = request.GET.get('page')

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

    ctx = {
        'buscadorF': buscadorF,
        'paisesF': paisesF,
        'moneda': moneda,
        'pais': pais,
        'inmuebles': inmuebles,
        'imagenes': imagenes,
    }

    return render_to_response('home/home.html', ctx, context_instance=RequestContext(request))


#Vista de cada inmueble
def inmueble(request, codigo, pais):

    envio = False

    #Buscador de inmuebles
    buscadorF = BuscadorForm()
    buscadorF.fields['ciudad'] = forms.ModelChoiceField(Ciudad.objects.filter(pais__nombre=pais), empty_label=' - Ciudad -')
    buscadorF.fields['zona'] = forms.ModelChoiceField(Zona.objects.filter(ciudad__pais__nombre=pais), empty_label=' - Zona -')

    #Inmueble
    inmueble = get_object_or_404(Inmueble, codigo=codigo)
    
    #Modulos
    modulos = Modulo.objects.filter(inmueble=inmueble).order_by('metros')

    #Agente
    agente = inmueble.agente
    telefonos = TelefonoAgente.objects.filter(agente=agente)

    #Contacto con el agente
    contactoF = ContactoAgenteForm()

    #Imagenes del inmueble
    imagenes = ImagenInmueble.objects.filter(inmueble=inmueble)

    #Moneda
    try:
        moneda = Moneda.objects.get(pais__nombre=pais)
    except:
        moneda = ''

    #Banners del home
    banners = Banner.objects.filter(pais__nombre=pais)

    if request.POST:
        contactoF = ContactoAgenteForm(request.POST)
        if contactoF.is_valid():
            envio = contact_email(request, contactoF, agente.correo)
            contactoF = ContactoAgenteForm()

    #Formulario para los paises disponibles
    paisesF = PaisesForm(initial={
        'pais': pais,
    })

    ctx = {
        'inmueble': inmueble,
        'modulos': modulos,
        'moneda': moneda,
        'buscadorF': buscadorF,
        'telefonosAgente':telefonos,
        'ContactoAgenteForm': contactoF,
        'paisesF': paisesF,
        'imagenes': imagenes,
        'banners': banners,
        'pais': pais,
        'envio': envio,
    }

    return render_to_response('inmuebles/inmueble.html', ctx, context_instance=RequestContext(request))


#Vista para el ingreso de los usuarios.
def login_admin(request, pais):

    username = ''
    password = ''
    buscadorF = BuscadorForm()
    buscadorF.fields['ciudad'] = forms.ModelChoiceField(Ciudad.objects.filter(pais__nombre=pais), empty_label=' - Ciudad -')
    buscadorF.fields['zona'] = forms.ModelChoiceField(Zona.objects.filter(ciudad__pais__nombre=pais), empty_label=' - Zona -')
   
    
    #Formularios basicos
    loginF = LoginForm()

    if request.user.is_authenticated() and request.user:
        
        return HttpResponseRedirect('/'+str(pais)+'/admin/perfil/')

    if request.method == "POST":

        loginF = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        usuario = authenticate(username=username, password=password)

        if usuario:
                # Caso del usuario activo
                if usuario.is_active:
                    login(request, usuario)
                    return HttpResponseRedirect('/'+str(pais)+'/admin/perfil/')
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


#Vista para el ingreso de los usuarios.
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
        'inmuebles':inmuebles,
        'agentes':agentes,
        'ciudades':ciudades,
        'zonas':zonas,
        'pais':pais,
        'nombre_pais':nombre_pais,
    }
    return render_to_response('admin/perfil.html', ctx, context_instance=RequestContext(request))


#Vista para listar los inmuebles de ese pais
@login_required
def inmuebles_list(request, pais):
    
    inmuebles = Inmueble.objects.filter(pais__nombre=pais)
    nombre_pais = dict(countries)[pais]

    ctx = {
        'inmuebles':inmuebles,
        'pais':pais,
        'nombre_pais':nombre_pais,
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
        context['pais'] = kwargs['pais']
        return context


#Vista para publicar el inmueble
class Publicar(CreateView):
    template_name = 'admin/inmuebles/publicar.html'
    model = Inmueble
    form = InmuebleForm
    # areacomunF = AreaComunForm()
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
              'fecha_entrega',
              'tipo_obra',
              'agente',
              'latitud',
              'longitud',
              'areas_comunes',
              'logo']

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        areacomunF = AreaComunForm()
        form.fields['agente'] = forms.ModelChoiceField(Agente.objects.filter(pais__nombre=kwargs["pais"]))
        form.fields['ciudad'] = forms.ModelChoiceField(Ciudad.objects.filter(pais__nombre=kwargs["pais"]))
        form.fields['zona'] = forms.ModelChoiceField(Zona.objects.filter(ciudad__pais__nombre=kwargs["pais"]))
        form.fields['areas_comunes'] = forms.ModelMultipleChoiceField(AreaComun.objects.all(), widget=forms.CheckboxSelectMultiple())
        tipo = get_object_or_404(TipoInmueble, id=kwargs["tipo"])
        campos = CampoTipoInmueble.objects.filter(tipo_inmueble=tipo)
        ValorCampoTipoInmuebleFormset = inlineformset_factory(Inmueble,
                                                              ValorCampoTipoInmueble,
                                                              extra=campos.count(),
                                                              can_delete=False,
                                                              min_num=campos.count(),
                                                              max_num=campos.count(),
                                                              fields=['campo', 'valor'])
        return self.render_to_response(self.get_context_data(form=form, pais=kwargs["pais"]))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.fields['agente'] = forms.ModelChoiceField(Agente.objects.filter(pais__nombre=kwargs["pais"]))
        form.fields['ciudad'] = forms.ModelChoiceField(Ciudad.objects.filter(pais__nombre=kwargs["pais"]))
        form.fields['zona'] = forms.ModelChoiceField(Zona.objects.filter(ciudad__pais__nombre=kwargs["pais"]))
        form.fields['areas_comunes'] = forms.ModelMultipleChoiceField(AreaComun.objects.all(), widget=forms.CheckboxSelectMultiple())
        tipo = get_object_or_404(TipoInmueble, id=kwargs["tipo"])
        campos = CampoTipoInmueble.objects.filter(tipo_inmueble=tipo)
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
            return self.form_invalid(form, kwargs["pais"])

    def form_valid(self, form, tipo, pais):
        self.object = form.save(commit=False)
        self.object.pais = Pais.objects.get(nombre=pais)
        self.object.tipo = tipo
        self.object.fecha_expiracion = datetime.now()
        self.object.save()
        return redirect('inmuebles:listar_inmuebles', pais=pais)

    def form_invalid(self, form,  pais):
        return self.render_to_response(
            self.get_context_data(form=form, pais=pais))


#Vista para publicar el inmueble
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


#Vista para publicar el inmueble
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


#Vista para agregar los agentes de ese pais
@login_required
def modulos_eliminar(request, pais, id_inmueble, id_modulo):
    modulo = get_object_or_404(Modulo, id=id_modulo).delete()

    return redirect('inmuebles:detalle', pais=pais, id_inmueble=id_inmueble)


#Vista para agregar los agentes de ese pais
@login_required
def inmuebles_editar(request, pais, id_inmueble):
    
    editado = ''
    inmueble = Inmueble.objects.get(id=id_inmueble)
    inmuebleF = InmuebleForm(instance=inmueble)

    if request.POST:
        inmuebleF = InmuebleForm(request.POST, request.FILES, instance=inmueble)
        if inmuebleF.is_valid():
            inmuebleF.save()
            editado = True

    ctx = {
        'InmuebleForm':inmuebleF,
        'editado':editado,
        'pais':pais,
    }
    
    return render_to_response('admin/inmuebles/editar.html', ctx, context_instance=RequestContext(request))


#Vista para agregar las imagenes del inmueble
def inmuebles_imagenes(request, pais, id_inmueble):

    editado = ''
    inmueble = Inmueble.objects.get(id=id_inmueble)
    imagenes = ImagenInmueble.objects.filter(inmueble=inmueble)
    #Formset de imagen
    ImagenFormset = inlineformset_factory(Inmueble, ImagenInmueble, form = ImagenInmuebleForm, can_delete=True, extra=1, max_num=len(imagenes)+2, fields=['imagen', 'descripcion'])
    inmuebleF = ImagenFormset(instance=inmueble, queryset=ImagenInmueble.objects.filter(inmueble=inmueble))

    if request.POST:
        inmuebleF = ImagenFormset(request.POST, request.FILES, instance=inmueble)
        if inmuebleF.is_valid():
            inmuebleF.save()

    inmuebleF = ImagenFormset(instance=inmueble, queryset=ImagenInmueble.objects.filter(inmueble=inmueble))
    ctx = {
        'InmuebleForm':inmuebleF,
        'editado':editado,
        'pais':pais,
    }

    return render_to_response('admin/inmuebles/imagenes-inmueble.html', ctx, context_instance=RequestContext(request))


#Vista para agregar los agentes de ese pais
@login_required
def inmuebles_eliminar(request, pais, id_inmueble):
    
    inmueble = get_object_or_404(Inmueble, id=id_inmueble).delete()

    return HttpResponseRedirect('/'+str(pais)+'/admin/inmuebles/')

#Vista para listar los agentes de ese pais
@login_required
def agentes_list(request, pais):
    
    agentes = Agente.objects.filter(pais__nombre=pais)
    nombre_pais = dict(countries)[pais]

    ctx = {
        'agentes':agentes,
        'pais':pais,
        'nombre_pais':nombre_pais,
    }
    
    return render_to_response('admin/agentes/agentes.html', ctx, context_instance=RequestContext(request))


#Vista para agregar los agentes de ese pais
@login_required
def agentes_agregar(request, pais):
    
    agenteF = AgenteForm()
    telefonoFormSet = inlineformset_factory(Agente, TelefonoAgente, extra=4, max_num=4, form = TelefonoAgenteForm, can_delete = True)
    telefonoAgenteF = telefonoFormSet()

    if request.POST:
        agenteF = AgenteForm(request.POST, request.FILES)
        telefonoFormSet = inlineformset_factory(Agente, TelefonoAgente, extra=4, max_num=4, form = TelefonoAgenteForm, can_delete = True)
        telefonoAgenteF = telefonoFormSet(request.POST)
        if agenteF.is_valid() and telefonoAgenteF.is_valid():
            agente = agenteF.save(commit=False)
            pais = Pais.objects.get(nombre=pais)
            agente.pais = pais
            agente.save()

            #Verificacion de telefonos del agente
            for form in telefonoAgenteF:

                #Verificar que se llenaron los numeros
                try:
                    numero  = form.cleaned_data['numero']
                except:
                    numero = ''

                if numero != '':
                    telefono = form.save(commit=False)
                    telefono.agente = agente
                    telefono.save()

            return HttpResponseRedirect('/'+str(pais)+'/admin/agentes/')

    ctx = {
        'TelefonoAgenteForm': telefonoAgenteF,
        'AgenteForm':agenteF,
        'pais':pais,
    }
    
    return render_to_response('admin/agentes/agregar.html', ctx, context_instance=RequestContext(request))


#Vista para agregar los agentes de ese pais
@login_required
def agentes_editar(request, pais, id_agente):
    
    editado = ''
    agente = Agente.objects.get(id=id_agente)
    agenteF = AgenteForm(instance=agente)
    telefonoFormSet = inlineformset_factory(Agente, TelefonoAgente, extra=4, max_num=4, form = TelefonoAgenteForm, can_delete = True)
    telefonoAgenteF = telefonoFormSet(instance=agente)

    if request.POST:
        agenteF = AgenteForm(request.POST, request.FILES, instance=agente)
        telefonoFormSet = inlineformset_factory(Agente, TelefonoAgente, extra=4, max_num=4, form = TelefonoAgenteForm, can_delete = True)
        telefonoAgenteF = telefonoFormSet(request.POST, instance=agente)
        if agenteF.is_valid() and telefonoAgenteF.is_valid():
            agenteF.save()
            telefonoAgenteF.save()
            editado = True

    telefonoFormSet = inlineformset_factory(Agente, TelefonoAgente, extra=4, max_num=4, form = TelefonoAgenteForm, can_delete = True)
    telefonoAgenteF = telefonoFormSet(instance=agente)

    ctx = {
        'AgenteForm':agenteF,
        'TelefonoAgenteForm': telefonoAgenteF,
        'editado':editado,
        'pais':pais,
    }
    
    return render_to_response('admin/agentes/editar.html', ctx, context_instance=RequestContext(request))


#Vista para agregar los agentes de ese pais
@login_required
def agentes_eliminar(request, pais, id_agente):
    
    agente = get_object_or_404(Agente, id=id_agente).delete()

    return HttpResponseRedirect('/'+str(pais)+'/admin/agentes/')


#Vista para listar las ciudades de ese pais
@login_required
def ciudades_list(request, pais):
    
    ciudades = Ciudad.objects.filter(pais__nombre=pais)
    nombre_pais = dict(countries)[pais]

    ctx = {
        'ciudades':ciudades,
        'pais':pais,
        'nombre_pais':nombre_pais,
    }
    
    return render_to_response('admin/ciudades/ciudades.html', ctx, context_instance=RequestContext(request))


#Vista para agregar las ciudades de ese pais
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

            return HttpResponseRedirect('/'+str(pais)+'/admin/ciudades/')

    ctx = {
        'CiudadForm':ciudadF,
        'pais':pais,
    }

    return render_to_response('admin/ciudades/agregar.html', ctx, context_instance=RequestContext(request))


#Vista para agregar las ciudades de ese pais
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
        'CiudadForm':ciudadF,
        'editado':editado,
        'pais':pais,
    }

    return render_to_response('admin/ciudades/editar.html', ctx, context_instance=RequestContext(request))


#Vista para agregar los agentes de ese pais
@login_required
def ciudades_eliminar(request, pais, id_ciudad):
    
    ciudad = get_object_or_404(Ciudad, id=id_ciudad).delete()

    return HttpResponseRedirect('/'+str(pais)+'/admin/ciudades/')


#Vista para listar las ciudades de ese pais
@login_required
def zonas_list(request, pais):
    
    zonas = Zona.objects.filter(ciudad__pais__nombre=pais)
    nombre_pais = dict(countries)[pais]

    ctx = {
        'zonas':zonas,
        'pais':pais,
        'nombre_pais':nombre_pais,
    }
    
    return render_to_response('admin/zonas/zonas.html', ctx, context_instance=RequestContext(request))


#Vista para agregar las ciudades de ese pais
@login_required
def zonas_agregar(request, pais):
    
    zonaF = ZonaForm()
    
    if request.POST:
        zonaF = ZonaForm(request.POST)
        if zonaF.is_valid():
            zonaF.save()

            return HttpResponseRedirect('/'+str(pais)+'/admin/zonas/')

    zonaF.fields['ciudad'] = forms.ModelChoiceField(Ciudad.objects.filter(pais__nombre=pais), empty_label=' - Ciudad -')

    ctx = {
        'ZonaForm':zonaF,
        'pais':pais,
    }
    
    return render_to_response('admin/zonas/agregar.html', ctx, context_instance=RequestContext(request))


#Vista para agregar las ciudades de ese pais
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
        'ZonaForm':zonaF,
        'editado':editado,
        'pais':pais,
    }
    
    return render_to_response('admin/zonas/editar.html', ctx, context_instance=RequestContext(request))


#Vista para agregar los agentes de ese pais
@login_required
def zonas_eliminar(request, pais, id_zona):
    
    zona = get_object_or_404(Zona, id=id_zona).delete()

    return HttpResponseRedirect('/'+str(pais)+'/admin/zonas/')


#Vista para listar las ciudades de ese pais
@login_required
def monedas_list(request, pais):
    
    try:
        moneda = Moneda.objects.get(pais__nombre=pais)
    except:
        moneda = ''

    nombre_pais = dict(countries)[pais]

    ctx = {
        'moneda':moneda,
        'pais':pais,
        'nombre_pais':nombre_pais,
    }
    
    return render_to_response('admin/monedas/monedas.html', ctx, context_instance=RequestContext(request))


#Vista para agregar las ciudades de ese pais
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

            return HttpResponseRedirect('/'+str(pais)+'/admin/monedas/')

    ctx = {
        'MonedaForm':monedaF,
        'pais':pais,
    }
    
    return render_to_response('admin/monedas/agregar.html', ctx, context_instance=RequestContext(request))


#Vista para agregar las ciudades de ese pais
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
        'MonedaForm':monedaF,
        'editado':editado,
        'pais':pais,
    }
    
    return render_to_response('admin/monedas/editar.html', ctx, context_instance=RequestContext(request))


#Vista para agregar los agentes de ese pais
@login_required
def monedas_eliminar(request, pais, id_moneda):
    
    moneda = get_object_or_404(Moneda, id=id_moneda).delete()

    return HttpResponseRedirect('/'+str(pais)+'/admin/monedas/')



#Vista para cerrar la sesion
@login_required
def logout_admin(request, pais):

    logout(request)
    return HttpResponseRedirect('/'+str(pais)+'/')
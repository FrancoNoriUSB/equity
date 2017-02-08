# -*- coding: utf-8 -*-
from django.core.mail.message import EmailMessage
from django.db.models import Q

# Set de funciones varias a utilizar en el frontend


# Funcion para los correos que se envian en Contact Us
def contact_email(request, form, correo, inmueble):

    emailF = form
    emails = []

    # Informacion del usuario
    name = emailF.cleaned_data['nombre']
    emails.append(correo)
    emails.append('coordinacion@equitymedia.la')
    emails.append('fernandoweber@equitymedia.la')
    emails.append('info@equitymedia.la')
    telephone = emailF.cleaned_data['telefonos']

    # Verificacion de si posee telefono
    if telephone == '':
        telephone = 'No posee telefono de contacto.'

    # Mensaje a enviar
    message = 'Correo de contacto del usuario: ' + str(name) + '. Con correo: ' + str(emailF.cleaned_data['correo']) + '<br>'
    message += 'Inmueble: ' + inmueble.titulo + '<br>'
    message += 'Mensaje: ' + str(emailF.cleaned_data['comentario']) + '<br>'
    message += 'Telefono de contacto: ' + str(telephone)

    email = EmailMessage()
    email.subject = '[Equity International] Correo contacto'
    email.body = message
    email.to = emails
    email.content_subtype = "html"
    enviado = email.send()
    return enviado


# Funcion para los correos que se envian en Contact Us
def visit_email(request, form, inmueble):

    emailF = form
    emails = []

    # Informacion del usuario
    name = emailF.cleaned_data['nombre']
    emails.append('contactcenter@equitymedia.la')
    emails.append('fernandoweber@equitymedia.la')
    emails.append('info@equitymedia.la')
    telephone = emailF.cleaned_data['telefonos']

    # Verificacion de si posee telefono
    if telephone == '':
        telephone = 'No posee telefono de contacto.'

    # Mensaje a enviar
    message = 'Correo de solicitud de visita del usuario: ' + str(name) + '. Con correo: ' + str(emailF.cleaned_data['correo']) + '<br>'
    message += 'Inmueble: ' + inmueble.titulo
    message += 'Fecha: ' + str(emailF.cleaned_data['fecha_cita']) + '<br>'
    message += 'Telefono de contacto: ' + str(telephone)

    email = EmailMessage()
    email.subject = '[Equity International] Correo Visita'
    email.body = message
    email.to = emails
    email.content_subtype = "html"
    enviado = email.send()
    return enviado


# Funcion para enviar favoritos del usuario via correo
def favoritos_email(request, user, favoritos):

    emails = []
    emails.append(user.email)

    message = '<h3>Resumen de inmuebles favoritos Equity International</h3><br><br>'
    message += '<table><thead><tr><th>País</th><th>Ciudad</th><th>Inmueble</th><th>M2</th><th>Hab</th></tr></thead>'

    for favorito in favoritos:
        message += '<tr><td>' + str(favorito.modulo.inmueble.pais.nombre.encode('UTF-8', 'strict')) + '</td><td>' + str(favorito.modulo.inmueble.ciudad.nombre.encode('UTF-8', 'strict')) + '</td><td>' + str(favorito.modulo.inmueble.titulo.encode('UTF-8', 'strict')) + '</td><td>' + str(favorito.modulo.metros.encode('UTF-8', 'strict')) + '</td><td>' + str(favorito.modulo.dormitorios.encode('UTF-8', 'strict')) + '</td></tr>'

    message += '</table>'

    email = EmailMessage()
    email.subject = '[Equity International] Resumen Favoritos'
    email.body = message
    email.to = emails
    email.content_subtype = "html"
    enviado = email.send()
    return enviado


# Funcion para los correos que se envian en Contact Us
def movil_email(request, form, inmueble):

    emailF = form
    emails = []

    # Informacion del usuario
    emails.append('contactcenter@equitymedia.la')
    emails.append('fernandoweber@equitymedia.la')
    emails.append('info@equitymedia.la')

    # Mensaje a enviar
    message = 'Correo de solicitud de visita de usuario con correo: ' + str(emailF.cleaned_data['correo']) + '<br>'
    message += 'Inmueble: ' + inmueble.titulo

    email = EmailMessage()
    email.subject = '[Equity International] Correo Visita'
    email.body = message
    email.to = emails
    email.content_subtype = "html"
    enviado = email.send()
    return enviado


# Query dinamico extraido de un proyecto ajeno
def dynamic_query(model, fields, types, values, operator):
    """
     Takes arguments & constructs Qs for filter()
     We make sure we don't construct empty filters that would
        return too many results
     We return an empty dict if we have no filters so we can
        still return an empty response from the view
    """

    queries = []
    for (f, t, v) in zip(fields, types, values):
        # We only want to build a Q with a value
        if v is not None:
            if t == 'range':
                kwargs = {str('%s__%s' % (f, t)): (v)}
            else:
                kwargs = {str('%s__%s' % (f, t)): str('%s' % v)}
            queries.append(Q(**kwargs))

    # Make sure we have a list of filters
    if len(queries) > 0:
        q = Q()
        # AND/OR awareness
        for query in queries:
            if operator == "and":
                q = q & query
            elif operator == "or":
                q = q | query
            else:
                q = None
        if q:
            return model.objects.filter(q)
            # We have a Q object, return the QuerySet
    else:
        # Return an empty result
        return {}

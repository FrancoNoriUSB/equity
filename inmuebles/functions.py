from django.core.mail.message import EmailMessage
from django.db.models import Count
from django.db.models import Q

#Set de funciones varias a utilizar en el frontend

#Funcion para los correos que se envian en Contact Us
def contact_email(request, form, correo):

    emailF = form
    emails = []

    #Informacion del usuario
    name = emailF.cleaned_data['nombre']
    emails.append(correo)
    emails.append('equity@equitymedia.la')
    telephone = emailF.cleaned_data['telefonos']

    #Verificacion de si posee telefono
    if telephone == '':
        telephone = 'No posee telefono de contacto.'

    #Mensaje a enviar
    message = 'Correo de contacto del usuario: '+ str(name) +'. Con correo: ' + str(emailF.cleaned_data['correo']) +'<br>'
    message += 'Mensaje: '+ str(emailF.cleaned_data['comentario']) + '<br>'
    message += 'Telefono de contacto: '+ str(telephone)

    email = EmailMessage()
    email.subject = '[Equity International] Correo contacto'
    email.body = message
    email.from_email = 'Usuario Equity <'+str(emailF.cleaned_data['correo'])+'>'
    email.to = emails
    email.content_subtype = "html"
    enviado=email.send()
    return True

#Query dinamico extraido de un proyecto ajeno
def dynamic_query(model, fields, types, values, operator, order):
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
        if v != None: 
            if t == 'range':
                kwargs = {str('%s__%s' % (f,t)) : (v)}
            else:
                kwargs = {str('%s__%s' % (f,t)) : str('%s' % v)}
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
        if q and order != None:
            # We have a Q object, return the QuerySet
            if order == 'precio':
                return model.objects.filter(q).order_by('modulo')
            elif order == 'tipo':
                return model.objects.filter(q).order_by('tipo__nombre')
            elif order == 'zona':
                return model.objects.filter(q).order_by('zona__nombre')
            elif order == 'metros':
                return model.objects.filter(q).order_by('modulo__metros')

            return model.objects.filter(q)
        elif q:
            # We have a Q object, return the QuerySet
            return model.objects.filter(q)
    else:
        # Return an empty result
        return {}
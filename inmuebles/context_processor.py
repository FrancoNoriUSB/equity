# -*- coding: utf-8 -*-
from inmuebles.models import *
from inmuebles.forms import *


def context_busqueda(request):
    buscadorF = BuscadorForm()
    return {'buscadorF': buscadorF}

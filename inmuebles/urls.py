from django.conf.urls import *
from django.conf import settings

#Urls para los views del frontend del usuario visitante
urlpatterns = patterns('inmuebles.views',
	url(r'^$', 'index', name='index'),
	url(r'^pais/(?P<pais>.*)$', 'home', name='home'),
)
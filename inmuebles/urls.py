from django.conf.urls import *

#Urls para los views del frontend del usuario visitante
urlpatterns = patterns('inmuebles.views',
	url(r'^$', 'index', name='index'),
)
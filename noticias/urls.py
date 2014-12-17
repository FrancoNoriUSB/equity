import django.conf.urls

# Urls para los views del frontend del usuario visitante
urlpatterns = django.conf.urls.patterns('noticias.views',
                                        django.conf.urls.url(r'^noticia/$', 'noticia', name='noticia'),
)
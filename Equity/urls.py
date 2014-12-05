from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Equity.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r'^$', 'inmuebles.views.index', name='index'),

    url(r'^admin/', include(admin.site.urls)),

    #Urls de los inmuebles de Equity
    url(r'^', include('inmuebles.urls')),

    #Urls de las noticias de Equity
#    url(r'^', include('noticias.urls')),

    url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT,}),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
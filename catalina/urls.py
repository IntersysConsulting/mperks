from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from meijer import views 

urlpatterns = patterns('',
    url(r'^$', 'meijer.views.index', name='index'),
    url(r'^index/$' , 'meijer.views.index'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^signin/$' , 'meijer.views.signin'),
    url(r'^signout/$' , 'meijer.views.signout'),
    url(r'^create_or_update/$' , 'meijer.views.create_or_update'),
    url(r'^newuser/$' , 'meijer.views.newuser'),
    url(r'^rewards/$' , 'meijer.views.rewards'),
    url(r'^activate/$' , 'meijer.views.activate'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

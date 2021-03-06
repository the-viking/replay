# from django.conf.urls.defaults import *
from django.conf import settings
from django.conf.urls import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('play.views',
    url(r'^$', 'home'),
    url(r'^user/(\d+)/', 'user'),
    url(r'^add/$', 'add'),
    url(r'^item/(\d+)/', 'item'),
    url(r'^delete/(\d+)/', 'delete'),
    url(r'^edit/(\d+)/', 'edit'),
    url(r'^notify/(\d+)/', 'notify'),
    url(r'^community/$', 'community'),
    url(r'^logout/$', 'logout_user'),
    url(r'^account/$', 'account'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^ask/$', 'ask', name="ask"),
    url(r'^ask/(\d+)/', 'ask', name="ask"),
    url(r'^about/', 'about'),
    url(r'^contact/', 'contact'),
    # url(r'^replay/', include('replay.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

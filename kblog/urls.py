from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('blog.views',
    # Examples:
    # url(r'^$', 'knd2blog.views.home', name='home'),
    # url(r'^knd2blog/', include('knd2blog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','home_blogs'),
    url(r'^index/$','home_blogs'),
    url(r'^blog/(\d+)/$','show_blog'),
    url(r'^menu/(?P<year>\d{4})/(?P<month>\d{2})/$','show_menu'),
    url(r'^menu/(?P<menuname>\w+)/$','show_menu'),
    url(r'^menu/$','show_menu'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.STATIC_ROOT,'show_indexes': True}),
    )

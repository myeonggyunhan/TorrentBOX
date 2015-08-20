from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TorrentBox.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('core.urls', namespace='core')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('account.urls', namespace='account')),
    url(r'^api/', include('api.urls', namespace='api')),

    # FIXED ISSUE: 404 Not Found error when Debug set to False (https://github.com/L34p/TorrentBOX/issues/2)
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG}),
)

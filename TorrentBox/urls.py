from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TorrentBox.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('core.urls', namespace='core')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('account.urls', namespace='account')),
    url(r'^api/', include('api.urls', namespace='api')),
)

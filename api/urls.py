from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

	url(r'^add_torrent/$', 'api.views.add_torrent', name='add_torrent'),
)

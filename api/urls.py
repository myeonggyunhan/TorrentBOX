from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

	url(r'^add_torrent/$', 'api.views.add_torrent', name='add_torrent'),
	url(r'^torrent_status/$', 'api.views.torrent_status', name='torrent_status'),
	url(r'^download/$', 'api.views.download', name='download'),
	url(r'^delete/$', 'api.views.delete', name='delete'),
)

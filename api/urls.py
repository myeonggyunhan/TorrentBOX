from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

	url(r'^add_torrent/$', 'api.views.add_torrent', name='add_torrent'),
	url(r'^list_progress/$', 'api.views.list_progress', name='list_progress'),
	url(r'^download/$', 'api.views.download', name='download'),
	url(r'^delete/$', 'api.views.delete', name='delete'),
	url(r'^debug/$', 'api.views.debug', name='debug'),
)

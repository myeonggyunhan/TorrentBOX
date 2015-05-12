from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

	url(r'^$', 'core.views.home', name='home'),
	url(r'^list_progress/$', 'core.views.list_progress', name='progress'),
)

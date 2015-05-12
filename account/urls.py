from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

	url(r'^sign_in/$', 'account.views.sign_in', name='sign_in'),
	url(r'^sign_up/$', 'account.views.sign_up', name='sign_up'),
	url(r'^sign_out/$', 'account.views.sign_out', name='sign_out'),
)

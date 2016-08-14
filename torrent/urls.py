from django.conf.urls import url

from . import views

app_name = 'torrent'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.add, name='add'),
    url(r'^status/$', views.status, name='status'),
]

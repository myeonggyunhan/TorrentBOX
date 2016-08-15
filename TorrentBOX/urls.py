from django.conf.urls import include, url
from django.contrib import admin

from torrent import views as torrent_view

urlpatterns = [
    url(r'^$', torrent_view.index),
    url(r'^admin/', admin.site.urls),
    url(r'^torrent/', include('torrent.urls')),
    url(r'^accounts/', include('accounts.urls')),
]

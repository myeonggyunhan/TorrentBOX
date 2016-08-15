import os

import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

import libtorrent as lt
from sendfile import sendfile

from .models import Torrent
from .tasks import download_torrent
from .utils import filesize, get_remain_time


@login_required
def index(request):
    torrents = Torrent.objects.get_actives(request.user)
    return render(request, 'torrent/index.html', {'torrents': torrents})

@login_required
def status(request):
    status_list = list()
    torrents = Torrent.objects.get_actives(request.user)

    for torrent in torrents:
        rtime = get_remain_time(torrent.size, torrent.downloaded_size, torrent.download_rate)
        status = dict(
            id = torrent.id,
            name = torrent.name,
            size = filesize(torrent.size),
            peers = torrent.peers,
            status = torrent.status,
            progress = torrent.progress,
            download_rate = filesize(torrent.download_rate, suffix='B/s'),
            downloaded_size = filesize(torrent.downloaded_size),
            rtime = rtime
        )

        status_list.append(status)

    return JsonResponse(status_list, safe=False)

@login_required
def download(request, torrent_id):
    torrent = get_object_or_404(Torrent, id=torrent_id, owner=request.user)

    # User can download only finished file
    if torrent.status == "finished":
        filepath = os.path.join(settings.SENDFILE_ROOT, torrent.name)
        return sendfile(request, filepath, attachment=True, attachment_filename=torrent.name)

    else:
        messages.error(request, "You can't download file until finished")
        return redirect('torrent:index')
   
@login_required
def delete(request, torrent_id):
    torrent = get_object_or_404(Torrent, id=torrent_id, owner=request.user)

    # Delete torrent entry but not delete real file in the server
    if torrent.status == 'finished':
        torrent.delete()
    
    # Torrent entry will be deleted by celery task
    elif torrent.status == 'downloading':
        torrent.status = 'terminated'
        torrent.save()

    elif torrent.status == 'queued':
        torrent.status = 'terminated'
        torrent.save()
        # XXX: Torrent is in the ready queue.
        # TODO: Add eviction functionality.

    return redirect('torrent:index')

@login_required
def add(request):
    # TODO: URL validation, Support magnet URI
    if 'torrent_file' in request.FILES:
        torrent_file = request.FILES['torrent_file']
        torrent_data = torrent_file.read()

    elif 'torrent_url' in request.POST:
        url = request.POST['torrent_url']
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        torrent_data = response.content

    else:
        return redirect('torrent:index')

    e = lt.bdecode(torrent_data)
    info = lt.torrent_info(e)
    torrent_hash = str(info.info_hash())

    # Current user already have this torrent
    if Torrent.objects.filter(owner=request.user, hash=torrent_hash).exists():
        return redirect('torrent:index')

    # Finished torrent file is already exist in the server
    exist_torrent = Torrent.objects.filter(hash=torrent_hash, status='finished').first()
    if exist_torrent:
        Torrent.objects.copy_and_create(exist_torrent, request.user)
        return redirect('torrent:index')

    new_torrent = Torrent.objects.create(
        name = info.name(),
        hash = torrent_hash,
        size = int(info.total_size()),
        peers = 0,
        status = 'queued',
        progress = 0,
        download_rate = 0,
        downloaded_size = 0,
        owner = request.user
    )

    download_torrent.delay(new_torrent.id, torrent_data)
    return redirect('torrent:index')

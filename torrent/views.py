from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

import libtorrent as lt
import requests

from .models import Torrent
from .tasks import download_torrent

@login_required
def index(request):
    # TODO: List torrent entry
    return render(request, 'torrent/index.html')

@login_required
def status(request):
    # TODO: Show current status of torrents
    return render(request, 'torrent/index.html')

@login_required
def download(request):
    # TODO: Send torrent file to user
    return render(request, 'torrent/index.html')

@login_required
def delete(request):
    # TODO: Delete torrent entry
    return render(request, 'torrent/index.html')

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

    e = lt.bdecode(torrent_data)
    info = lt.torrent_info(e)
    torrent_hash = str(info.info_hash())

    # Current user already have this torrent
    if Torrent.objects.filter(owner=request.user, hash=torrent_hash).exists():
        return redirect('torrent:index')

    # Finished torrent file is already exist in the server
    exist_torrent = Torrent.objects.filter(hash=torrent_hash, status="finished").first()
    if exist_torrent:
        Torrent.objects.copy_and_create(request.user)
        return redirect('torrent:index')

    new_torrent = Torrent.objects.create(
        name = info.name(),
        hash = torrent_hash,
        size = int(info.total_size()),
        peers = 0,
        status = "queued",
        progress = 0,
        download_rate = 0,
        downloaded_size = 0,
        owner = request.user
    )

    download_torrent.delay(new_torrent.id, torrent_data)
    return redirect('torrent:index')


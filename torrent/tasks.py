import time

from celery.decorators import task
from django.conf import settings

import libtorrent as lt

from .models import Torrent


@task(name='download_torrent')
def download_torrent(torrent_id, torrent_data):
    ses = lt.session()
    ses.listen_on(6881, 6891)
    e = lt.bdecode(torrent_data)
    info = lt.torrent_info(e)
    h = ses.add_torrent({'ti': info, 'save_path': settings.TORRENT_STORAGE})

    # Torrent is not valid
    if not h.is_valid():
        #TODO: Send error message to user
        return

    while (not h.is_seed()):
        # XXX: Performance issue?... access database every loop
        torrent = Torrent.objects.get(id = torrent_id)

        # Torrent is canceled by user during download
        if torrent.status == 'terminated':
            torrent.delete()
            return

        s = h.status()
        torrent.peers = s.num_peers
        torrent.progress = int(s.progress * 100)
        torrent.status = 'downloading'
        torrent.download_rate = s.download_rate
        torrent.downloaded_size = s.total_done
        torrent.save()
        time.sleep(2)

    # TODO: If downloaded file is directory, then zip (change status to "compressing")

    # Download is done
    torrent.peers = 0
    torrent.progress = 100
    torrent.download_rate = 0
    torrent.downloaded_size = torrent.size
    torrent.status = 'finished'
    torrent.save()

    return

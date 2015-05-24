from djcelery import celery
import signal
import os
import time
import sys
from account.models import Account, TorrentEntries
from django.contrib.auth.models import User
from django.conf import settings

TorrentStorage_PATH = settings.DOWNLOAD_DIR
download_flag=True

#TODO: more effecient method?...
def receive_signal(signum, stack):
	global download_flag	
	print "[!] Received exit signal: " + str(signum)
	download_flag=False



@celery.task(name='tasks.TorrentDownload')
def TorrentDownload(username, mode, data):
	import libtorrent as lt
	import urllib2
	import time

	#TODO: We have to support Three mode, URL, magnet, File
	# register signal
	signal.signal(signal.SIGINT, receive_signal)
	
	global download_flag	
	download_flag=True

	ses = lt.session()
	ses.listen_on(6881, 6891)


	#TODO: Current only support url
	url = data
	response = urllib2.urlopen(url)
	e = lt.bdecode(response.read())

	info = lt.torrent_info(e)
	info_hash = info.info_hash()

	h = ses.add_torrent({'ti': info, 'save_path': TorrentStorage_PATH})
	if h.is_valid() is not True:
		print "[!] Not valid torrent!"
		return

	# Save progress and torrent download status into DB
	u = User.objects.get(username = username)
	account = Account.objects.get(user=u)
	new_entry=TorrentEntries(name=str(h.name()), hash_value=str(info_hash), progress=0, download_rate=0, owner=account, file_size=int(h.status().total_wanted), downloaded_size=0, peers=0, status="download", worker_pid=os.getpid())
	try:
		new_entry.save()
	except:
		print "[!] Database insert Error"
		return

	while (not h.is_seed() and download_flag is True):
		s = h.status()
		new_entry.progress=float("%.2f" % (s.progress * 100))
		new_entry.download_rate=s.download_rate
		new_entry.downloaded_size=s.total_done
		new_entry.peers=s.num_peers
		new_entry.save()
		time.sleep(1);

	# User cancel torrent download during downloading...
	if download_flag is False:
		new_entry.delete()
	else:
		print "[+] Done: " + str(h.name())
		new_entry.progress=100
		new_entry.downloaded_size = new_entry.file_size
		new_entry.download_rate = 0
		new_entry.peers = 0
		new_entry.status="finished"
		new_entry.save()


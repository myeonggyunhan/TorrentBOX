from djcelery import celery
import signal
import os
import time
import sys
from account.models import Account, TorrentEntries, TorrentGlobalEntries
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from utils.func import *
import shutil

TorrentStorage_PATH = settings.DOWNLOAD_DIR
download_flag=True

#TODO: more effecient method?...
def receive_signal(signum, stack):
	global download_flag	
	download_flag=False

@celery.task(name='tasks.TorrentDownload')
def TorrentDownload(account, data):
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
	e = lt.bdecode(data)
	info = lt.torrent_info(e)
	info_hash = info.info_hash()

	#TODO: if torrent_entry progress is not 100.0 ?...
	# instead duplicated download, we have to provide mirror of one 
	# actually download only one torrent, others just get information of it not download it

	# Add torrent
	h = ses.add_torrent({'ti': info, 'save_path': TorrentStorage_PATH})
	
	# Torrent validation check
	if h.is_valid() is not True:
		print "[ERROR] Not valid torrent!"
		return

	# Save progress and torrent download status into DB
	new_entry=TorrentEntries(name=str(h.name()), hash_value=str(info_hash), 
				progress=0, download_rate=0, owner=account, 
				file_size=int(h.status().total_wanted), downloaded_size=0, 
				peers=0, status="initializing", worker_pid=os.getpid())
	try:
		new_entry.save()
	except:
		print "[ERROR] Database insert Error"
		return

	while (not h.is_seed() and download_flag is True):
		s = h.status()
		new_entry.progress=int("%d" % (s.progress * 100))
		new_entry.download_rate=s.download_rate
		new_entry.downloaded_size=s.total_done
		new_entry.peers=s.num_peers
		new_entry.status="downloading"
		new_entry.save()
		time.sleep(1);

	filePath = os.path.join(TorrentStorage_PATH,new_entry.name)

	# User cancel torrent download during downloading...
	if download_flag is False:
		new_entry.delete()
	else:
		if os.path.isdir(filePath):
			# make folder to zip file
			new_entry.status="compressing"
			new_entry.save()
			compress_data(TorrentStorage_PATH, new_entry.name)
			
			# remove original directory
			shutil.rmtree(filePath)	
			new_entry.name = new_entry.name + ".zip"

		print "[INFO] Done: " + str(h.name())
		new_entry.progress=100
		new_entry.downloaded_size = new_entry.file_size
		new_entry.download_rate = 0
		new_entry.peers = 0
		new_entry.status="finished"
		new_entry.save()

		global_entry=TorrentGlobalEntries(name=new_entry.name,
						hash_value=new_entry.hash_value,
						progress=new_entry.progress,
						file_size=new_entry.file_size,
						downloaded_size=new_entry.downloaded_size,
						peers=new_entry.peers,
						status=new_entry.status)
		global_entry.save()



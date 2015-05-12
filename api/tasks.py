from djcelery import celery
import signal
import os
import time
import sys
from account.models import Account, TorrentEntries
from django.contrib.auth.models import User

TorrentStorage_PATH = "/home/leap/Django/TorrentBox/static/TorrentStorage"
download_flag=True

def receive_signal(signum, stack):
	global download_flag	
	print "[!] Received exit signal: " + str(signum)
	#TODO: more effecient method?...
	#TODO: Post Action... remove file, db update, etc...
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
	new_entry=TorrentEntries(name=str(h.name()), hash_value=str(info_hash), progress=0, download_rate=0, owner=account)
	try:
		new_entry.save()
	except:
		print "[!] Error"
		return

	while (not h.is_seed() and download_flag is True):
		s = h.status()
		print "[+] Name: " + str(h.name()) + " / PID: " + str(os.getpid())
		print "[+] progress : %.2f%%" % (s.progress*100)
		print "[+] Down speed: %.1f kb/s" %(s.download_rate / 1000)
		new_entry.progress=float("%.2f" % (s.progress * 100))
		new_entry.download_rate=float("%.1f" % (s.download_rate / 1000))
		new_entry.save()
		time.sleep(3);

	print "[+] Done: " + str(h.name())
	new_entry.progress=100
	new_entry.save()


import libtorrent as lt
import urllib2
import time
import sys

import requests

ses = lt.session()
ses.listen_on(6881, 6891)

response = requests.get(sys.argv[1])
e = lt.bdecode(response.content)
info = lt.torrent_info(e)

h = ses.add_torrent({'ti': info, 'save_path': './'})
print 'starting', h.name()

while (not h.is_seed()):
   s = h.status()

   state_str = ['queued', 'checking', 'downloading metadata', \
      'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']
   print '\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
      (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
      s.num_peers, state_str[s.state]),
   sys.stdout.flush()
   test_progress = s.progress * 100
   print "\n[+] test progress: %d" % test_progress
   print "[+] total download: " + str(s.total_download)
   print "[+] total done: " + str(s.total_done)
   print "[+] total wanted done: " + str(s.total_wanted_done)
   print "[+] total wanted: " + str(s.total_wanted)
   if s.download_rate != 0:
      print "[!] Remaining time? -> " + str((s.total_wanted-s.total_done) / s.download_rate) + "sec"

   time.sleep(1)

print "[+] total download: " + str(s.total_download)
print "[+] total done: " + str(s.total_done)
print "[+] total wanted done: " + str(s.total_wanted_done)
print "[+] total wanted: " + str(s.total_wanted)
print h.name(), 'complete'

time.sleep(10)
print "[+] total done: " + str(s.total_done)
print "[+] total wanted done: " + str(s.total_wanted_done)

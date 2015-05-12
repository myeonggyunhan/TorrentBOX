# TorrentBOX
Multi-user based Torrent Download and Sharing Web Service

아직 아주 기본적인 부분만 구현되어있고, 고칠부분이 많이 있습니다 ㅠㅠ..

We need at least two Terminal

python manage.py runserver 0.0.0.0:8000
python manage.py celeryd -l info -c 2

celeryd -c option means total number of worker
If we set -c option to 2, then we can download two torrent simultaneously.

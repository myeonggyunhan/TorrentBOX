# TorrentBOX
Multi-user based torrent download and sharing application written in Django  

## Screenshot
![Demo](https://cloud.githubusercontent.com/assets/8179234/17862249/670f204e-68cf-11e6-81e8-feb0214786dc.png)

## Prerequisites
* [libtorrent](http://www.libtorrent.org/) - [[Install guide](https://github.com/L34p/TorrentBOX/wiki/Installation-guide-for-libtorrent-1.1.0)]
* [RabbitMQ](https://www.rabbitmq.com/)    - [[Install guide](https://github.com/L34p/TorrentBOX/wiki/Installation-guide-for-RabbitMQ)]

## Installation
```bash
$ git clone https://github.com/L34p/TorrentBOX.git
$ cd TorrentBOX
$ pip3 install -r requirements.txt
$ python3 manage.py migrate
```

## Quick Start
* Two terminals are needed.  
* [Concurrency option](http://docs.celeryproject.org/en/latest/userguide/workers.html#concurrency) determines the number of torrent that can be downloaded simultaneously.  
```bash
# First terminal
$ python3 manage.py runserver 0.0.0.0:8000

# Second terminal  
$ python3 manage.py celeryd --loglevel info --concurrency 5
```
**NOTE:** This is only for test. If you want to deploy it, use Django with other web servers like [Apache](http://www.apache.org/) or [Nginx](http://nginx.org/).

## License
[MIT](LICENSE.md)

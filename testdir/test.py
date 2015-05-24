torrent_list = []

torrent_info = {}
torrent_info['hash_value'] = "e8765ae0454c086acd7aa375151581c78df8e8aa"
torrent_info['name'] = "[Leopard-Raws] Danna ga Nani o Itteiru ka Wakaranai Ken 2 Sureme - 08 RAW (TVS 1280x720 x264 AAC).mp4"
torrent_list.append(dict(torrent_info))

torrent_info['hash_value'] = "1923674927836498726498726349872634987623"
torrent_info['name'] = "[Leopard-Raws] Danna ga Nani o Itteiru ka Wakaranai Ken 2 Sureme - 01 RAW (TVS 1280x720 x264 AAC).mp4"
torrent_list.append(dict(torrent_info))

for entry in torrent_list:
	print entry['hash_value']


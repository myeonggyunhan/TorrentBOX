from django.shortcuts import render, render_to_response, RequestContext, redirect
from time import sleep
from api import tasks

def add_torrent(request):

	if request.POST.has_key('mode') is True:
		mode = request.POST['mode']
		#if request.POST.has_key('url') is True and mode=="url":
		if request.POST.has_key('url') is True:
			url = request.POST['url']
			tasks.TorrentDownload.delay(request.user.username, mode, url)

			# TODO: It is not good way... 
			sleep(1)	
			return redirect("/")

		else:
			print "DEBUG:: Not support yet..."
			return redirect("/")
	else:
		print "DEBUG:: Error"
		return redirect("/")
		
	return redirect("/")


	

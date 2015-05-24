from django.shortcuts import HttpResponse, render, render_to_response, RequestContext, redirect
from django.contrib.auth.decorators import login_required
from account.models import Account, TorrentEntries
from django.core.servers.basehttp import FileWrapper
from django.contrib.auth.models import User
from django.conf import settings
from utils.func import *
from time import sleep
from api import tasks
import os
import signal

@login_required
def add_torrent(request):

	if request.POST.has_key('mode') is True:
		mode = request.POST['mode']
		#if request.POST.has_key('url') is True and mode=="url":
		if request.POST.has_key('url') is True:
			url = request.POST['url']
			tasks.TorrentDownload.delay(request.user.username, mode, url)

			return redirect("/")

		else:
			print "DEBUG:: Not support yet..."
			return redirect("/")
	else:
		print "DEBUG:: Error"
		return redirect("/")
		
	return redirect("/")

@login_required
def list_progress(request):
        u = User.objects.get(username=request.user.username)
        current_account = Account.objects.get(user=u)
        try:
                entries = TorrentEntries.objects.filter(owner=current_account)
        except:
                entries = None
        
	torrent_list = []
        torrent_info = {}

        for entry in entries:
                torrent_info['hash_value'] = entry.hash_value
                torrent_info['name'] = entry.name
                torrent_info['progress'] = entry.progress
		torrent_info['peers'] = entry.peers

                torrent_info['download_rate'] = unitConversion(entry.download_rate, "download_rate")
                torrent_info['file_size'] = unitConversion(entry.file_size, "file")
                torrent_info['downloaded_size'] = unitConversion(entry.downloaded_size, "file")

	
		if entry.status == "finished":
			torrent_info['rtime'] = "Finished!"
       
	        elif entry.download_rate == 0:
                        torrent_info['rtime'] = "remaining time unknown"
        
	        else:
                        rtime = (entry.file_size - entry.downloaded_size) / entry.download_rate
                        torrent_info['rtime'] = unitConversion(rtime, "time") + " remaining"

                torrent_list.append(dict(torrent_info))

        return render_to_response("list_progress.html", locals(), context_instance=RequestContext(request))

@login_required
def download(request):

	# Error handling, redirect to root
	if request.GET.has_key('torrent_hash') is not True:
		return redirect("/")

	torrent_hash = request.GET.get('torrent_hash','')
        u = User.objects.get(username=request.user.username)
        current_account = Account.objects.get(user=u)
        try:
                entry = TorrentEntries.objects.get(owner=current_account, hash_value=torrent_hash)
        except:
                entry = None
		return redirect("/")

	# If download is not completed yet, redirect to root
	# TODO: we have to notice this to user
	if entry.progress != 100.0:
		return redirect("/")

	filename = settings.DOWNLOAD_DIR + str(entry.name)
	wrapper = FileWrapper(file(filename))
	response = HttpResponse(wrapper, content_type='application/octet-stream')
	response['Content-Disposition'] = 'attachment; filename=' + str(entry.name)
	response['Content-Length'] = os.path.getsize(filename)

	return response	

@login_required
def delete(request):
		
	# Error handling, redirect to root
	if request.GET.has_key('torrent_hash') is not True:
		return redirect("/")

	torrent_hash = request.GET.get('torrent_hash','')
        u = User.objects.get(username=request.user.username)
        current_account = Account.objects.get(user=u)
        try:
                entry = TorrentEntries.objects.get(owner=current_account, hash_value=torrent_hash)
        except:
                entry = None
		return redirect("/")

	# If progress is 100%, then delete TorrentEntry from user DB
	# However, we don't delete real file from server
	if entry.progress == 100.0:
		entry.delete()

	# User cancel torrent download during download ...	
	else:
		os.kill(entry.worker_pid, signal.SIGINT)

	return redirect("/")

def debug(request):
	
        u = User.objects.get(username=request.user.username)
        current_account = Account.objects.get(user=u)
        try:
                entries = TorrentEntries.objects.filter(owner=current_account)
        except:
                entries = None

	torrent_list = []
	torrent_info = {}
	
	for entry in entries:
		print entry.hash_value
		torrent_info['hash_value'] = entry.hash_value
		torrent_info['name'] = entry.name

		# Custome DATA
		torrent_info['rtime'] = 300
		torrent_list.append(dict(torrent_info))


        return render_to_response("debug.html", locals(), context_instance=RequestContext(request))

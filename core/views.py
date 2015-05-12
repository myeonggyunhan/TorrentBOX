# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, RequestContext, redirect
from django.http import HttpResponse
from account.models import Account, TorrentEntries
from core.models import Entries
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

@login_required
def home(request):
	template = "index.html"	
	
	username = request.user.username
	#print "DEBUG:: Current user: " + str(username)
	
	u = User.objects.get(username=request.user.username)
	current_account = Account.objects.get(user=u)

	entries = TorrentEntries.objects.filter(owner=current_account)
	try:
		entries = TorrentEntries.objects.filter(owner=current_account)
	except:
		entries = None

	''' debug
	for entry in entries:
		print entry.name
	'''
	return render_to_response(template,locals(),context_instance=RequestContext(request))

@login_required
def list_progress(request):
	u = User.objects.get(username=request.user.username)
	current_account = Account.objects.get(user=u)

	try:
		entries = TorrentEntries.objects.filter(owner=current_account)
	except:
		entries = None

	return render_to_response("list_progress.html", locals(), context_instance=RequestContext(request))

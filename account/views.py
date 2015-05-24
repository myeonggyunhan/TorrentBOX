from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import TorrentBoxCreateForm, TorrentBoxAuthForm


def sign_in(request):
	form = TorrentBoxAuthForm(data = request.POST or None)
	template = 'account/sign_in.html'

	next_url = request.POST.get("next", "/")

	if request.method == 'POST' and form.is_valid():
		login(request, form.get_user())
		
		return redirect(next_url)

	return render(request, template, {'form':form, 'next':next_url, })

def sign_up(request):
	form = TorrentBoxCreateForm(data = request.POST or None) 
	template = 'account/sign_up.html'

	if request.method == 'POST':
		if form.is_valid():
			username = form.clean_username()
			password = form.clean_password2()
			new_user = form.save()
			user = authenticate(username=username, password=password)
			login(request, user)
			
			return redirect("/")
		else:
			return render(request, template, {'form':form, })
			
	return render(request, template, {'form':form, })

@login_required
def sign_out(request):
	logout(request)

	return redirect("/")

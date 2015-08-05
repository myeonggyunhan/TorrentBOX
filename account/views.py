from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import TorrentBoxCreateForm, TorrentBoxAuthForm

def sign_in(request):
	auth_form = TorrentBoxAuthForm(data = request.POST or None)
	create_form = TorrentBoxCreateForm(data = request.POST or None) 
	template = 'account/sign_in.html'
	next_url = request.POST.get("next", "/")

	if request.method == 'POST' and auth_form.is_valid():
		login(request, auth_form.get_user())
		return redirect(next_url)

	return render(request, template, {'signin_form':auth_form, 'signup_form':create_form, 'next':next_url, })

def sign_up(request):
	auth_form = TorrentBoxAuthForm(data = request.POST or None)
	create_form = TorrentBoxCreateForm(data = request.POST or None) 
	template = 'account/sign_in.html'
	next_url = request.POST.get("next", "/")
	
	if request.method == 'POST':
		if create_form.is_valid():
			username = create_form.clean_username()
			password = create_form.clean_password2()
			new_user = create_form.save()
			user = authenticate(username=username, password=password)
			login(request, user)
			
			return redirect("/")
		else:
			return render(request, template, {'signin_form':auth_form, 'signup_form':create_form, 'next':next_url, })
			
	return render(request, template, {'signin_form':auth_form, 'signup_form':create_form, 'next':next_url, })


@login_required
def sign_out(request):
	logout(request)

	return redirect("/")

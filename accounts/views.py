from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import TorrentBoxAuthForm, TorrentBoxCreateForm


def sign_in(request):
    auth_form = TorrentBoxAuthForm(data=request.POST or None)
    create_form = TorrentBoxCreateForm(data=request.POST or None)
    template = 'accounts/sign_in.html'
    next_url = request.POST.get('next', '/')

    context = {
        'signin_form': auth_form,
        'signup_form': create_form,
        'next': next_url,
    }

    if request.method == 'POST':
        if auth_form.is_valid():
            login(request, auth_form.get_user())
            return redirect(next_url)
        else:
            messages.error(request, "Incorrect e-mail or password!")
            return render(request, template, context)

    return render(request, template, context)

def sign_up(request):
    auth_form = TorrentBoxAuthForm(data=request.POST or None)
    create_form = TorrentBoxCreateForm(data=request.POST or None)
    template = 'accounts/sign_in.html'
    next_url = request.POST.get('next', '/')

    context = {
        'signin_form': auth_form,
        'signup_form': create_form,
        'next': next_url,
    }

    if request.method == 'POST':
        if create_form.is_valid():
            username = create_form.clean_username()
            password = create_form.clean_password2()
            new_user = create_form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('torrent:index')
        else:
            messages.error(request, "Invalid registration form")
            return render(request, template, context)

    else:
        return render(request, template, context)

@login_required
def sign_out(request):
    logout(request)
    return redirect('accounts:sign_in')

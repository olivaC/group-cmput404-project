from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from SocialDistribution import settings
from app.forms.registration_forms import LoginForm
from app.utilities import unquote_redirect_url


@login_required
def index(request):
    print('yar')
    user = request.user
    request.context['user'] = user
    return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            redirect_url = request.POST.get('next', reverse("app:index"))
            return HttpResponseRedirect(unquote_redirect_url(redirect_url))
        else:
            request.context['next'] = unquote_redirect_url(request.GET.get('next', reverse("web:index")))
    else:
        request.context['next'] = request.GET.get('next', '')
        form = LoginForm()
    request.context['form'] = form
    request.context['path'] = settings.DOMAIN
    return render(request, 'login.html', request.context)


@login_required
def logout_view(request):
    """
    View used for logging out.

    :param request:
    :return: The index page.
    """
    logout(request)
    return HttpResponseRedirect(request.GET.get(next, reverse("app:index")))

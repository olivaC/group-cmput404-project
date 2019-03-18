from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from app.models import Author


@login_required
def all_author_view(request):
    user = request.user
    authors = Author.objects.all().order_by('username')
    request.context['user'] = user
    request.context['authors'] = authors

    return render(request, 'authors/all_authors.html', request.context)


@login_required
def follow_view(request, id):
    current_author = request.user.user
    auth = Author.objects.filter(id=id).first()
    if auth:
        current_author.add(auth)
        current_author.save()
    return HttpResponseRedirect(reverse("app:all_authors"))

@login_required
def unfollow_view(request, id):
    current_author = request.user.user
    auth = Author.objects.filter(id=id).first()
    if auth:
        current_author.add(auth)
        current_author.save()
    return HttpResponseRedirect(reverse("app:all_authors"))

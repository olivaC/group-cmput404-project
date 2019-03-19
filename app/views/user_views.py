from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from app.models import Author, FollowRequest


@login_required
def all_author_view(request):
    user = request.user
    current_author = request.user.user
    authors = Author.objects.all().order_by('username')
    request.context['user'] = user
    request.context['authors'] = authors
    following = FollowRequest.objects.all().filter(author=current_author)
    request.context['following'] = following

    return render(request, 'authors/all_authors.html', request.context)


@login_required
def follow_view(request, id):
    current_author = request.user.user
    auth = Author.objects.filter(id=id).first()
    if auth:
        FollowRequest.objects.create(
            author=current_author,
            friend=auth
        )
    return HttpResponseRedirect(reverse("app:all_authors"))


@login_required
def unfollow_view(request, id):
    current_author = request.user.user
    auth = Author.objects.filter(id=id).first()
    unfollow = FollowRequest.objects.all().filter(author=current_author).filter(friend=auth)
    if unfollow:
        unfollow.delete()
    return HttpResponseRedirect(reverse("app:following"))


@login_required
def new_followers_view(request):
    current_author = request.user.user
    followers_new = FollowRequest.objects.all().filter(friend=current_author).filter(acknowledged=False)

    for follow in followers_new:
        follow.acknowledged = True
        follow.save()

    request.context['followers_new'] = followers_new

    return render(request, 'authors/follower_request.html', request.context)


@login_required
def all_followers_view(request):
    current_author = request.user.user
    followers = FollowRequest.objects.all().filter(friend=current_author)

    request.context['followers'] = followers

    return render(request, 'authors/followers.html', request.context)


@login_required
def all_following_view(request):
    current_author = request.user.user
    following = FollowRequest.objects.all().filter(author=current_author)

    request.context['following'] = following

    return render(request, 'authors/following.html', request.context)

import json

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from urllib.parse import urlparse
from datetime import datetime
from pytz import utc

from api.api_utilities import remoteAddAuthor
from app.models import *
from django.db.models.functions import Lower

from app.utilities import api_check, create_author


@login_required
@user_passes_test(api_check)
def all_author_view(request):
    user = request.user
    current_author = request.user.user
    authors = Author.objects.all().order_by(Lower('username')).exclude(id=current_author.id)
    request.context['user'] = user
    request.context['authors'] = authors

    f_request = FriendRequest.objects.all().filter(author=current_author).values('friend')
    pending = Author.objects.all().filter(id__in=f_request)

    request.context['pending'] = pending

    friends = request.user.user.friends.all()
    request.context['friends'] = friends

    return render(request, 'authors/all_authors.html', request.context)


@login_required
@user_passes_test(api_check)
def follow_view(request, id):
    current_author = request.user.user
    auth = Author.objects.filter(id=id).first()
    if auth:
        FollowRequest.objects.create(
            author=current_author,
            friend=auth
        )

    auth_follow = FollowRequest.objects.all().filter(friend=current_author).filter(author=auth)
    if auth_follow:
        current_author.friends.add(auth)
        current_author.save()

    app_url = request.path

    if 'authors' in app_url:
        return HttpResponseRedirect(reverse("app:all_authors"))
    elif 'followers' in app_url:
        return HttpResponseRedirect(reverse("app:followers"))


@login_required
@user_passes_test(api_check)
def unfollow_view(request, id):
    current_author = request.user.user
    auth = Author.objects.filter(id=id).first()
    unfollow = FollowRequest.objects.all().filter(author=current_author).filter(friend=auth)
    if unfollow:
        unfollow.delete()
        current_author.friends.remove(auth)
        current_author.save()
    return HttpResponseRedirect(reverse("app:following"))


@login_required
@user_passes_test(api_check)
def unfollow_mutual_view(request, id):
    current_author = request.user.user
    auth = Author.objects.filter(id=id).first()
    # unfollow = FollowRequest.objects.all().filter(author=current_author).filter(friend=auth)
    # if unfollow:
    #     unfollow.delete()
    current_author.friends.remove(auth)
    current_author.save()
    return HttpResponseRedirect(reverse("app:mutual_friends"))


@login_required
@user_passes_test(api_check)
def new_followers_view(request):
    current_author = request.user.user
    followers_new = FollowRequest.objects.all().filter(friend=current_author).filter(acknowledged=False)

    for follow in followers_new:
        follow.acknowledged = True
        follow.save()

    request.context['followers_new'] = followers_new

    return render(request, 'authors/follower_request.html', request.context)


@login_required
@user_passes_test(api_check)
def all_followers_view(request):
    current_author = request.user.user
    followers = FollowRequest.objects.all().filter(friend=current_author)
    following = FollowRequest.objects.all().filter(author=current_author).values('friend')
    followings = Author.objects.all().filter(id__in=following)

    request.context['followers'] = followers
    request.context['followings'] = followings

    return render(request, 'authors/followers.html', request.context)


@login_required
@user_passes_test(api_check)
def all_requests_view(request):
    current_author = request.user.user
    f_requests = FriendRequest.objects.all().filter(friend=current_author)
    r_requests = RemoteFriendRequest.objects.all().filter(friend=current_author)

    all_requests = list(f_requests)
    remote_requests = list()

    if r_requests:
        for r in r_requests:
            server = r.server
            auth_url = r.author
            req = requests.get(auth_url, auth=(server.username, server.password))
            if req.status_code != 200:
                continue
            else:
                author = create_author(req.json())
                friend = FriendRequest()
                friend.remote = 'remote'
                friend.author = author
                friend.friend = current_author
                friend.timestamp = r.timestamp

                remote_requests.append(friend)

    all_requests.extend(remote_requests)
    all_requests.sort(key=lambda yar: yar.timestamp, reverse=True)

    request.context['requests'] = all_requests

    return render(request, 'authors/following.html', request.context)


@login_required
def mutual_friends_view(request):
    friends = request.user.user.friends.all()
    posts = Post.objects.all().filter(author__id__in=friends).filter(visibility="FRIENDS") | Post.objects.all().filter(
        author__id__in=friends).filter(visibility="SERVERONLY") | Post.objects.all().filter(
        author__id__in=friends).filter(visibility="PUBLIC")
    request.context['friends'] = friends
    request.context['posts'] = posts
    return render(request, 'authors/mutual_friends.html', request.context)


def profile_remote_view(request):
    url = request.GET.get('host', '')
    url_parse = urlparse(url)
    req = "{}://{}".format(url_parse.scheme, url_parse.netloc)
    server = Server.objects.get(hostname__contains=req)

    try:
        if server.username and server.password:
            r = requests.get(url, auth=(server.username, server.password))
        else:
            r = requests.get(url)
    except:
        print("Error")

    if r.status_code == 200:
        a = create_author(r.json())
        a.remote = "remote"

        try:
            f_request = FriendRequest.objects.all().filter(author=a).values('friend')
            pending = Author.objects.all().filter(id__in=f_request)

            request.context['pending'] = pending

            friends = request.user.user.friends.all()
            request.context['friends'] = friends
        except:
            print('error remote user')
            return HttpResponseRedirect('index.html')

    request.context['author'] = a

    return render(request, 'profile.html', request.context)


def send_friend_request(request, id):
    current_author = request.user.user
    auth = Author.objects.filter(id=id).first()

    if auth:
        FriendRequest.objects.create(
            author=current_author,
            friend=auth
        )

    return HttpResponseRedirect(reverse("app:all_authors"))


def cancel_friend_request(request, id):
    current_author = request.user.user
    auth = Author.objects.filter(id=id).first()
    f_request = FriendRequest.objects.filter(friend=current_author, author=auth).first()
    f_request.delete()
    return HttpResponseRedirect(reverse("app:all_authors"))


def accept_friend_request(request, id):
    current_author = request.user.user
    auth = Author.objects.filter(id=id).first()
    f_request = FriendRequest.objects.filter(friend=current_author, author=auth).first()

    current_author.friends.add(auth)
    current_author.save()
    f_request.delete()

    return HttpResponseRedirect(reverse("app:mutual_friends"))


def accept_remote_friend_request(request):
    url = request.GET.get('id', '')
    url_parse = urlparse(url)
    req = "{}://{}".format(url_parse.scheme, url_parse.netloc)
    server = Server.objects.get(hostname__contains=req)

    current_author = request.user.user
    f_request = RemoteFriendRequest.objects.filter(friend=current_author, author=url).first()

    r = RemoteFriend.objects.create(author=current_author, friend=url, server=server)
    if r:
        f_request.delete()

    return HttpResponseRedirect(reverse("app:mutual_friends"))


def send_remote_friend_request(request, uuid):
    host = request.GET.get('host', '')
    server = Server.objects.get(hostname=host)

    server_api = server.hostname

    if server_api.endswith("/"):
        server_api = "{}author/{}".format(server.hostname, uuid)
    else:
        server_api = "{}/author/{}".format(server.hostname, uuid)

    try:
        if server.username and server.password:
            r = requests.get(server_api, auth=(server.username, server.password))
    except:
        print("Error")

    if r.status_code == 200:
        friend_obj = r.json()

        friend = {
            'id': friend_obj.get('id'),
            'host': friend_obj.get('host'),
            'displayName': friend_obj.get('displayName'),
            'url': friend_obj.get('url')
        }

        author_obj = request.user.user

        author = {
            'id': "{}/api/author/{}".format(DOMAIN, author_obj.id),
            'host': "{}/api/".format(author_obj.host_url),
            'displayName': author_obj.username,
            'url': "{}/api/author/{}".format(DOMAIN, author_obj.id)
        }

        data = {
            'query':'friendrequest',
            'author': author,
            'friend': friend,
        }
        friend_url = server.hostname
        if friend_url.endswith("/"):
            friend_url = "{}friendrequest".format(friend_url)
        else:
            friend_url = "{}/friendrequest".format(friend_url)
        headers = {'Content-type': 'application/json'}
        r = requests.post(friend_url, data=json.dumps(data), headers=headers,
                          auth=(server.username, server.password))

        if r.status_code == 200:
            print("friend request sent")
        else:
            print("Errors in friend request")

        return HttpResponseRedirect(reverse("app:index"))

    print("Errors author")

    return HttpResponseRedirect(reverse("app:index"))


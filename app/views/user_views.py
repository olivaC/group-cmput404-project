from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from app.models import Author, FollowRequest, Post
from django.db.models.functions import Lower

from app.utilities import api_check


@login_required
@user_passes_test(api_check)
def all_author_view(request):
    user = request.user
    current_author = request.user.user
    authors = Author.objects.all().order_by(Lower('username')).exclude(id=current_author.id)
    request.context['user'] = user
    request.context['authors'] = authors
    following = FollowRequest.objects.all().filter(author=current_author).values('friend')
    following = Author.objects.all().filter(id__in=following)
    request.context['following'] = following

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
    unfollow = FollowRequest.objects.all().filter(author=current_author).filter(friend=auth)
    if unfollow:
        unfollow.delete()
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
def all_following_view(request):
    current_author = request.user.user
    following = FollowRequest.objects.all().filter(author=current_author)

    request.context['following'] = following

    return render(request, 'authors/following.html', request.context)


@login_required
@user_passes_test(api_check)
def mutual_friends_view(request):
    friends = request.user.user.friends.all()
    posts = Post.objects.all().filter(author__id__in=friends).filter(visibility="FRIENDS") | Post.objects.all().filter(
        author__id__in=friends).filter(visibility="SERVERONLY") | Post.objects.all().filter(
        author__id__in=friends).filter(visibility="PUBLIC")
    request.context['friends'] = friends
    request.context['posts'] = posts
    return render(request, 'authors/mutual_friends.html', request.context)

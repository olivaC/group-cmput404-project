import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from SocialDistribution import settings
from app.forms.post_forms import PostCreateForm, CommentCreateForm
from app.models import *
from app.utilities import *

from app.serializers import PostSerializer
from app.utilities import *
import json
from datetime import datetime

from pytz import utc


@login_required
@user_passes_test(api_check)
def my_posts_view(request):
    user = request.user
    request.context['user'] = user

    posts = Post.objects.all().filter(author=user.user).order_by('-published')

    if request.method == 'POST':
        next = request.POST.get("next", reverse("app:index"))
        form = PostCreateForm(request.POST)
        try:
            if form.is_valid():
                if form.cleaned_data.get('text'):
                    Post.objects.create(author=user.user, text=form.cleaned_data.get('text'))
                    return HttpResponseRedirect(reverse('app:index'))
            request.context['next'] = next
            messages.warning(request, 'Cannot post something empty!')


        except:
            request.context['next'] = request.GET.get('next', reverse("app:index"))

    form = PostCreateForm()
    request.context['form'] = form
    request.context['posts'] = posts

    return render(request, 'posts/my_posts.html', request.context)


@login_required
@user_passes_test(api_check)
def delete_post(request, id=None):
    post = get_object_or_404(Post, id=id)

    try:
        if request.method == 'POST':
            form = PostCreateForm(request.POST)
            post.delete()
            # messages.success(request, 'Post deleted')
            return redirect('../../my-posts')

    except Exception as e:
        messages.warning(request, 'Post could not be deleted')

    form = PostCreateForm()
    request.context['form'] = form

    return render(request, 'posts/post_delete.html', request.context)


@login_required
@user_passes_test(api_check)
def edit_post(request, id=None):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        next = request.POST.get("next", reverse("app:my_posts"))
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post.title = form.cleaned_data.get('title')
            post.description = form.cleaned_data.get('description')
            post.visibility = form.cleaned_data.get('visibility')
            post.content = form.cleaned_data.get('content')
            post.unlisted = form.cleaned_data.get('unlisted')
            post.contentType = form.cleaned_data.get('contentType')

            visible_to = form.cleaned_data.get('visibleTo')
            authors = Author.objects.filter(id__in=visible_to)
            post.visibleTo.set(authors)

            post.save()
            return HttpResponseRedirect(reverse('app:my_posts'))

        else:
            messages.warning(request, 'Error editing your post')

    form = PostCreateForm(initial=model_to_dict(post))
    request.context['post'] = post
    request.context['form'] = form

    return render(request, 'posts/edit_post.html', request.context)


@login_required
@user_passes_test(api_check)
def create_post_view(request):
    user = request.user
    request.context['user'] = user

    if request.method == 'POST':
        next = request.POST.get("next", reverse("app:index"))
        form = PostCreateForm(request.POST)
        try:
            if form.is_valid():
                if form.cleaned_data.get('content'):
                    visible_to = form.cleaned_data.get('visibleTo')
                    authors = Author.objects.filter(id__in=visible_to)

                    post = Post.objects.create(author=user.user, content=form.cleaned_data.get('content'),
                                               description=form.cleaned_data.get('description'),
                                               title=form.cleaned_data.get('title'),
                                               visibility=form.cleaned_data.get('visibility'),
                                               unlisted=form.cleaned_data.get('unlisted'),
                                               contentType=form.cleaned_data.get('contentType'))

                    for author in authors:
                        post.visibleTo.add(author)

                    if "base64" in post.contentType:
                        post.title = post.id
                        post.save()
                    return HttpResponseRedirect(reverse('app:index'))
            request.context['next'] = next
            messages.warning(request, 'Cannot post something empty!')


        except Exception as e:
            print(e)
            request.context['next'] = request.GET.get('next', reverse("app:index"))

    form = PostCreateForm()
    request.context['form'] = form

    return render(request, 'posts/create_post.html', request.context)


@login_required
def create_image_view(request):
    """
    View for uploading an image

    :param request
    :return: Image File Path if Success, 500 otherwise.
    """
    if request.method == 'POST':
        if "file" in request.FILES:
            file = request.FILES["file"]
            mimeType = get_image_type(file.name)
            data = get_base64(mimeType, file)

            # Create a Post associated with the image
            request.POST = request.POST.copy()
            request.POST["title"] = "Image"
            request.POST["contentType"] = mimeType + ";base64"
            request.POST["content"] = data
            print(request.POST)
            return create_post_view(request)
        else:
            request.context['next'] = next
            messages.warning(request, 'Not valid image form!')

    form = PostCreateForm()
    request.context['form'] = form

    return render(request, 'posts/create_image.html', request.context)


@login_required
@user_passes_test(api_check)
def public_post_view(request):
    local_posts = Post.objects.all().filter(visibility="PUBLIC").order_by('-published')

    servers = Server.objects.all()
    public_posts = list()

    for server in servers:
        host = server.hostname
        if not server.hostname.endswith("/"):
            host = server.hostname + "/"
        server_api = "{}posts".format(host)
        try:
            if server.username and server.password:
                r = requests.get(server_api, auth=(server.username, server.password))
                p = create_posts(r.json())
                public_posts.extend(p)
        except:
            print("error")

    posts = public_posts + list(local_posts)
    posts.sort(key=lambda post: post.published, reverse=True)

    request.context['posts'] = posts

    return render(request, 'posts/public_posts.html', request.context)


@login_required
@user_passes_test(api_check)
def create_comment_view(request, id=None):
    post = get_object_or_404(Post, id=id)
    comments = Comment.objects.all().filter(post=post)
    remote_comments = RemoteComment.objects.all().filter(post=post)

    master_list = list(comments)

    if remote_comments:
        for i in remote_comments:
            try:
                server = i.server
                auth_url = i.author
                req = requests.get(auth_url, auth=(server.username, server.password))
                if req.status_code != 200:
                    continue
                else:
                    comment = Comment()
                    comment.author = create_author(req.json())
                    comment.comment = i.comment
                    comment.contentType = i.contentType
                    comment.content = comment.get_comment()
                    comment.id = i.id
                    comment.published = i.published
                    master_list.append(comment)


            except:
                print("problem with getting Author")

    master_list.sort(key=lambda master: master.published, reverse=True)

    if request.method == 'POST':
        next = request.POST.get("next", reverse("app:index"))
        form = CommentCreateForm(request.POST)
        try:
            if form.is_valid():
                if form.cleaned_data.get('comment'):
                    author = request.user.user
                    Comment.objects.create(post=post, author=author, comment=form.cleaned_data.get('comment'),
                                           contentType=form.cleaned_data.get('contentType'))
                    return HttpResponseRedirect(request.path)
            request.context['next'] = next
            messages.warning(request, 'Error commenting.')


        except:
            request.context['next'] = request.GET.get('next', request.path)

    form = CommentCreateForm()
    request.context['post'] = post
    request.context['form'] = form
    request.context['comments'] = master_list

    return render(request, 'posts/post_detail.html', request.context)


@login_required
@user_passes_test(api_check)
def remote_post_view(request, post):
    host = request.GET.get('host', '')
    print(host)
    server = Server.objects.get(hostname=host)

    server_api = server.hostname
    if server_api.endswith("/"):
        server_api = "{}posts/{}".format(server.hostname, post)
    else:
        server_api = "{}/posts/{}".format(server.hostname, post)

    try:
        if server.username and server.password:
            r = requests.get(server_api, auth=(server.username, server.password))
        else:
            r = requests.get(server_api)
    except:
        print("Error")

    if r.status_code == 200:
        p = create_post(r.json())
        c = create_comments(r.json())

    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        try:
            if form.is_valid():
                if form.cleaned_data.get('comment') and form.cleaned_data.get('contentType'):
                    local_author = request.user.user
                    author = dict()
                    url = "{}/api/posts/{}".format(DOMAIN, post)
                    author['id'] = "{}/api/author/{}".format(DOMAIN, local_author.id)
                    author['url'] = "{}/api/author/{}".format(DOMAIN, local_author.id)
                    author['host'] = "{}/api/".format(local_author.host_url)
                    author['displayName'] = local_author.username
                    if local_author.github_url:
                        author['github'] = local_author.github_url

                    comment_id = str(uuid.uuid1())
                    published = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                    commment_data = form.cleaned_data.get('comment')
                    contentType = form.cleaned_data.get('contentType')

                    comment = {
                        'author': author,
                        'comment': commment_data,
                        'contentType': contentType,
                        'published': published,
                        'id': comment_id

                    }

                    data = {
                        'query': 'addComment',
                        'post': url,
                        'comment': comment

                    }

                    req_url = "{}/comments".format(server_api)
                    headers = {'Content-type': 'application/json'}
                    r = requests.post(req_url, data=json.dumps(data), headers=headers,
                                      auth=(server.username, server.password))

                    if r.status_code == 200:
                        path = "{}?host={}".format(request.path, host)
                        return HttpResponseRedirect(path)
                    else:
                        messages.warning(request, "You actually can't comment on this post...")

        except Exception as e:
            print(e)
            request.context['next'] = request.GET.get('next', request.path)

    form = CommentCreateForm()
    request.context['post'] = p
    request.context['form'] = form
    request.context['comments'] = c

    return render(request, 'posts/remote_post_detail.html', request.context)


@login_required
@user_passes_test(api_check)
def foaf_posts_view(request):
    user = request.user
    request.context['user'] = user

    friends = request.user.user.friends.all()
    foaf_friends = set()
    if friends:
        for i in friends:
            foaf = i.friends.all()
            for j in foaf:
                if i != j:
                    foaf_friends.add(j.id)

    posts = Post.objects.all().filter(author__id__in=foaf_friends).filter(visibility="FOAF").order_by(
        '-published').exclude(author=user.user)

    posts = posts
    request.context['posts'] = posts

    return render(request, 'posts/foaf_posts.html', request.context)


@login_required
@user_passes_test(api_check)
def mutual_friends_posts_view(request):
    user = request.user
    request.context['user'] = user

    posts = Post.objects.all().filter(author__id__in=request.user.user.friends.all()).filter(
        visibility="FRIENDS") | Post.objects.all().filter(author__id__in=request.user.user.friends.all()).filter(
        visibility="SERVERONLY") | Post.objects.all().filter(author__id__in=request.user.user.friends.all()).filter(
        visibility="FOAF") | Post.objects.all().filter(author__id__in=request.user.user.friends.all()).filter(
        visibility="PUBLIC")

    current_author = request.user.user
    remote_friends = RemoteFriend.objects.all().filter(author=current_author.url)
    print(remote_friends)
    all_posts = list()
    all_posts.extend(posts)
    if remote_friends:
        for remote in remote_friends:
            try:
                raw_id = remote.url.split("/")[-1]
                if remote.server.hostname.endswith("/"):
                    url = "{}author/{}/posts".format(remote.server.hostname, raw_id)
                    # url = "{}author-mutual/posts".format(remote.server.hostname, )
                else:
                    url = "{}author/{}/posts".format(remote.server.hostname, raw_id)
                    # url = "{}/author-mutual/posts".format(remote.server.hostname)

                headers = {'X-AUTHOR-ID': str(request.user.user.id)}
                r = requests.get(url, auth=(remote.server.username, remote.server.password), headers=headers)
                if r.status_code != 200:
                    continue
                else:
                    p = create_posts(r.json())
                    all_posts.extend(p)

            except Exception as e:
                print(e)
    posts = sorted(all_posts, key=lambda k: k.published, reverse=True)
    request.context['posts'] = posts

    return render(request, 'posts/mutual_friend_posts.html', request.context)


@login_required
@user_passes_test(api_check)
def private_friends_posts_view(request):
    private_posts = Post.objects.all().filter(visibleTo=request.user.user).order_by('-published')

    # for server in servers:
    #     host = server.hostname
    #     if not server.hostname.endswith("/"):
    #         host = server.hostname + "/"
    #     server_api = "{}posts".format(host)
    #     try:
    #         if server.username and server.password:
    #             r = requests.get(server_api, auth=(server.username, server.password))
    #             p = create_posts(r.json())
    #             public_posts.extend(p)
    #     except:
    #         print("error")
    #
    # posts = public_posts + list(local_posts)
    posts = list(private_posts)
    posts.sort(key=lambda post: post.published, reverse=True)

    request.context['posts'] = posts

    return render(request, 'posts/private_posts.html', request.context)


def unlisted_post_view(request, id=None):
    post = get_object_or_404(Post, id=id)

    if post.unlisted:
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data, safe=False)
    else:
        return HttpResponse({}, content_type='application/json', status=404)

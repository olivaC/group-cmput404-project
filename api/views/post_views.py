import requests
from django.http import HttpResponse
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.settings import api_settings

from api.api_utilities import postList, postCreate, str2bool, get_public_posts, getRemotePost
from app.models import Post, Author, Server, RemoteFriend

import datetime

from rest_framework import permissions


# Taken from https://stackoverflow.com/a/37649438
class IsGetOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        # allow all GET requests
        if request.method == 'GET':
            return True

        # Otherwise, only allow authenticated requests
        # Post Django 1.10, 'is_authenticated' is a read-only attribute
        return request.user and request.user.is_authenticated


class PublicPostView(APIView):
    """
    /api/posts
    """

    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def get(self, request):
        remote_id = request.META.get('HTTP_X_AUTHOR_ID')
        response = dict()
        response['query'] = 'posts'
        try:
            remote = Server.objects.get(user=request.user)
            public = Post.objects.all().filter(visibility="PUBLIC").order_by('-published')

            if remote.no_posts:
                response['posts'] = []
                response['success'] = True
                response['message'] = 'Server admin restricted posts.'
                return Response(response, status=403)

            if remote.no_images:
                public = public.exclude(contentType="image/png;base64").exclude(contentType='image/jpeg;base64')

            posts = postList(public)

            if remote.hostname.endswith("/"):
                url = "{}author/{}".format(remote.hostname, remote_id)
            else:
                url = "{}/author/{}/friends/".format(remote.hostname, remote_id)
            req = requests.get(url, auth=(remote.username, remote.password))
            if req.status_code == 200:
                r = req.json()
                friends = r.get('friends')
                for i in friends:
                    get_id = i.get('id')
                    raw_id = get_id.split('/')[-1]
                    try:
                        auth = Author.objects.get(id=raw_id)
                        friend_posts = Post.objects.all().filter(author=auth).filter(visibility="FRIENDS")
                        if remote.no_images:
                            friend_posts = friend_posts.exclude(contentType="image/png;base64").exclude(
                                contentType='image/jpeg;base64')
                        friend_posts = postList(friend_posts)
                        posts.extend(friend_posts)

                    except:
                        print("No authors matched")
        except:
            print("Not a server user")
            public = Post.objects.all().filter(visibility="PUBLIC").order_by('-published')
            posts = postList(public)
            posts = get_public_posts(posts)
            # server = Server.objects.get(hostname=request.)

        posts = sorted(posts, key=lambda k: k['published'], reverse=True)
        page = self.paginate_queryset(posts)
        if page is not None:
            page = self.get_paginated_response(page)
        dat = page.data
        response['posts'] = dat.get('results')
        response['previous'] = dat.get('previous')
        response['next'] = dat.get('next')
        response['count'] = dat.get('count')
        return Response(response, status=200)

    def post(self, request):
        user = request.user
        response = dict()
        try:
            remote = Server.objects.get(user=user)
            if remote:
                response['query'] = 'addPost'
                response['success'] = False
                response['message'] = 'Not authorized to create posts'
                return Response(response, status=403)
            else:
                response['query'] = 'addPost'
                response['success'] = False
                response['message'] = 'Not authorized to create posts'
                return Response(response, status=403)
        except:
            author = user.user
            r = request.POST
            title = r.get('title')
            description = r.get('description')
            visibility = r.get('visibility')
            content = r.get('content')
            contentType = r.get('contentType')
            unlisted = str2bool(r.get('unlisted'))

            if title and description and visibility and content and contentType and (unlisted in [True, False]):
                post = Post.objects.create(
                    author=author, title=title, description=description, visibility=visibility, content=content,
                    contentType=contentType, unlisted=bool(unlisted)
                )
                if post:
                    response['query'] = 'addPost'
                    response['success'] = True
                    response['message'] = 'Post added'

                    return Response(response, status=200)
                else:
                    response['query'] = 'addPost'
                    response['success'] = False
                    response['message'] = 'Post failed to create'

                    return Response(response, status=500)
            else:
                response['query'] = 'addPost'
                response['success'] = False
                response['message'] = 'Missing fields'

                return Response(response, status=500)

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class AuthorVisiblePostView(APIView):
    """
    /author/posts

    For currently authenticated user
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        remote_id = request.META.get('HTTP_X_AUTHOR_ID')
        if remote_id:
            post_list = list()
            remote = Server.objects.get(user=request.user)
            if remote:
                posts = Post.objects.all().filter(visibility="PUBLIC").order_by('-published')
                post_list.extend(posts)
                if remote.hostname.endswith("/"):
                    url = "{}author/{}".format(remote.hostname, remote_id)
                else:
                    url = "{}/author/{}/friends/".format(remote.hostname, remote_id)
                req = requests.get(url, auth=(remote.username, remote.password))
                if req.status_code == 200:
                    r = req.json()
                    friends = r.get('friends')
                    for i in friends:
                        get_id = i.get('id')
                        raw_id = get_id.split('/')[-1]
                        try:
                            auth = Author.objects.get(id=raw_id)
                            friend_posts = Post.objects.all().filter(author=auth).filter(
                                visibility="FRIENDS") | Post.objects.all().filter(author=auth).filter(
                                visibility="PUBLIC")
                            if remote.no_images:
                                friend_posts = friend_posts.exclude(contentType="image/png;base64").exclude(
                                    contentType='image/jpeg;base64')

                            post_list.extend(friend_posts)

                        except:
                            print("No authors matched")
                    response = dict()
                    response['query'] = 'posts'
                    response['count'] = len(post_list)
                    response['posts'] = postList(post_list)
                    return Response(response, status=200)
        else:
            user = request.user
            posts = Post.objects.all().filter(author__id__in=request.user.user.friends.all()).filter(
                visibility="FRIENDS") | Post.objects.all().filter(
                author__id__in=request.user.user.friends.all()).filter(
                visibility="SERVERONLY") | Post.objects.all().filter(author=user.user) | Post.objects.all().filter(
                visibility="PUBLIC")
            posts = posts.order_by('-published')
        response = dict()
        response['query'] = 'posts'
        response['count'] = len(posts)
        response['posts'] = postList(posts)
        return Response(response, status=200)


class AuthorPostView(APIView):
    """
    author/<uuid:id>/posts

    All posts made by {AUTHOR_ID} visible to the currently authenticated user
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        author = get_object_or_404(Author, id=id)
        remote_id = request.META.get('HTTP_X_AUTHOR_ID')
        try:
            server = Server.objects.get(user=request.user)
            if server:
                response = dict()
                if server.no_posts:
                    response['posts'] = []
                    response['success'] = True
                    response['message'] = 'Server admin restricted posts.'
                    return Response(response, status=403)

                remote = RemoteFriend.objects.all().filter(author=author).filter(friend__icontains=remote_id)
                if remote:
                    posts = Post.objects.all().filter(author=author).filter(
                        visibility="PUBLIC") | Post.objects.all().filter(author=author).filter(visibility="FRIENDS")
                else:
                    posts = Post.objects.all().filter(author=author).filter(visibility="PUBLIC")

                posts = Post.objects.all().filter(author=author).filter(visibility="PUBLIC")
                if server.no_images:
                    posts = posts.exclude(contentType="image/png;base64").exclude(
                        contentType='image/jpeg;base64')
                post_list = postList(posts)
                response['posts'] = post_list
                response['count'] = len(post_list)
                response['query'] = 'posts'
                return Response(response, status=200)
        except:
            current = request.user.user

            response = dict()
            friends = current.friends.all()

            if author in friends:
                posts = Post.objects.all().filter(author=author).filter(
                    visibility="FRIENDS") | Post.objects.all().filter(author=author).filter(
                    visibility="PUBLIC") | Post.objects.all().filter(author=author).filter(
                    visibility="FOAF") | Post.objects.all().filter(author=author).filter(
                    visibility="SERVERONLY")
                posts = posts.order_by('-published')
                response['query'] = 'posts'
                response['posts'] = postList(posts)
                response['count'] = len(posts)
                return Response(response, status=200)
            elif author == current:
                posts = Post.objects.all().filter(author=author)
                posts = posts.order_by('-published')
                response = dict()
                response['count'] = len(posts)
                response['query'] = 'posts'
                response['posts'] = postList(posts)
                return Response(response, status=200)
            else:
                posts = Post.objects.all().filter(visibility="PUBLIC")
                posts = posts.order_by('-published')
                response['count'] = len(posts)
                response['query'] = 'posts'
                response['posts'] = postList(posts)
                return Response(response, status=200)


class SinglePostView(APIView):
    """
    posts/<uuid:id>

    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsGetOrIsAuthenticated,)

    def get(self, request, id):
        response = dict()
        response['query'] = 'posts'

        if not request.user.is_authenticated:
            post = Post.objects.get(id=id)
            if post.unlisted:
                if post.contentType in ['image/png;base64', 'image/jpeg;base64']:
                    response = post.get_content()
                    return HttpResponse(response)
                else:
                    post = postCreate(post)
                    response['success'] = True
                    response['posts'] = post
                    response['count'] = 1
                    response['message'] = 'Unlisted post'
                    return Response(response, status=200)

        try:
            post = Post.objects.get(id=id)
            if post.contentType in ['image/png;base64', 'image/jpeg;base64']:
                response = post.get_content()
                return HttpResponse(response)
            post = postCreate(post)
        except:
            post = getRemotePost(id)

        if post:
            # First check if public
            if post[0].get('visibility') == "PUBLIC":
                response['posts'] = post
                response['count'] = 1
                response['success'] = True
                return Response(response, status=200)

            else:
                # TODO: FIX THIS
                response['success'] = True
                response['posts'] = post
                response['count'] = 1
                response['message'] = 'Need to fix this'
                return Response(response, status=200)

        else:
            response['posts'] = []
            response['count'] = 0
            response['success'] = False
            response['message'] = 'Cannot find post'
            return Response(response, status=404)

    def put(self, request, id):

        response = dict()
        response['query'] = 'putPost'

        try:
            post = Post.objects.get(id=id)
            try:
                server = Server.objects.get(user=request.user)
                if server:
                    response['success'] = False
                    response['message'] = "Not authorized to edit this post"
                    return Response(response, status=403)
            except:
                authenticated_author = request.user.user
                if authenticated_author != post.author:
                    response['success'] = False
                    response['message'] = "Not authorized to edit this post"
                    return Response(response, status=403)
                else:
                    r = request.POST
                    title = r.get('title')
                    description = r.get('description')
                    visibility = r.get('visibility')
                    content = r.get('content')
                    contentType = r.get('contentType')
                    unlisted = str2bool(r.get('unlisted'))

                    if title and description and visibility and content and contentType and (unlisted in [True, False]):
                        post.published = datetime.datetime.now()
                        post.title = title
                        post.description = description
                        post.visibility = visibility
                        post.content = content
                        post.contentType = contentType
                        post.unlisted = unlisted
                        post.save()

                        response['success'] = True
                        response['message'] = 'Post edited'

                        return Response(response, status=200)
                    else:
                        response['success'] = False
                        response['message'] = "Failed to edit post"
                        return Response(response, status=500)

        except:
            try:
                server = Server.objects.get(user=request.user)
                if server:
                    response['success'] = False
                    response['message'] = "Not authorized to add posts"
                    return Response(response, status=403)
            except:
                authenticated_author = request.user.user

                r = request.POST
                title = r.get('title')
                description = r.get('description')
                visibility = r.get('visibility')
                content = r.get('content')
                contentType = r.get('contentType')
                unlisted = str2bool(r.get('unlisted'))

                if title and description and visibility and content and contentType and (unlisted in [True, False]):
                    post = Post.objects.create(id=id,
                                               author=authenticated_author, title=title, description=description,
                                               visibility=visibility,
                                               content=content, contentType=contentType, unlisted=bool(unlisted)
                                               )
                    if post:
                        response['success'] = True
                        response['message'] = 'Post added'
                        return Response(response, status=200)
                    else:
                        response['query'] = 'addPost'
                        response['success'] = False
                        response['message'] = 'Post failed to put'
                        return Response(response, status=500)


class AuthorMutualPostView(APIView):
    """
    /author-mutual/posts

    For currently authenticated user
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        remote_id = request.META.get('HTTP_X_AUTHOR_ID')
        if remote_id:
            post_list = list()
            remote = Server.objects.get(user=request.user)
            if remote:
                if remote.hostname.endswith("/"):
                    url = "{}author/{}".format(remote.hostname, remote_id)
                else:
                    url = "{}/author/{}/friends/".format(remote.hostname, remote_id)
                req = requests.get(url, auth=(remote.username, remote.password))
                if req.status_code == 200:
                    r = req.json()
                    friends = r.get('friends')
                    for i in friends:
                        get_id = i.get('id')
                        raw_id = get_id.split('/')[-1]
                        try:
                            auth = Author.objects.get(id=raw_id)
                            friend_posts = Post.objects.all().filter(author=auth).filter(
                                visibility="FRIENDS") | Post.objects.all().filter(author=auth).filter(
                                visibility="PUBLIC")
                            post_list.extend(friend_posts)

                        except:
                            print("No authors matched")
                    response = dict()
                    response['query'] = 'posts'
                    response['count'] = len(post_list)
                    response['posts'] = postList(post_list)
                    return Response(response, status=200)
        else:
            user = request.user
            posts = Post.objects.all().filter(author__id__in=request.user.user.friends.all()).filter(
                visibility="FRIENDS") | Post.objects.all().filter(
                author__id__in=request.user.user.friends.all()).filter(
                visibility="SERVERONLY") | Post.objects.all().filter(author=user.user) | Post.objects.all().filter(
                visibility="PUBLIC")
            posts = posts.order_by('-published')
        response = dict()
        response['query'] = 'posts'
        response['count'] = len(posts)
        response['posts'] = postList(posts)
        return Response(response, status=200)

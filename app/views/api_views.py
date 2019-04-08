from rest_framework import viewsets
from rest_framework import permissions

from app.serializers import *
from django.shortcuts import render
from django.urls import reverse
from app.forms.post_forms import AuthorForm
import json
import requests
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from app.models import Author


class AuthorView(viewsets.ModelViewSet):
    """
    The api view to retrieve author.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers


class UserView(viewsets.ModelViewSet):
    """
    The api view to retrieve user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostView(viewsets.ModelViewSet):
    """
    The api view to retrieve posts.
    """
    serializer_class = PostSerializer
    allowed_methods = ['GET', 'POST', 'PATCH']

    def get_queryset(self):

        if self.request.user.is_anonymous:
            return Post.objects.all().filter(visibility="PUBLIC")
        else:
            author = self.request.user.user
            posts = Post.objects.all().filter(author=author) | Post.objects.all().filter(visibility="PUBLIC")
            posts = posts.order_by('-published')
            return posts


class AuthorPostView(viewsets.ModelViewSet):
    """
    The api view to retrieve posts.
    """
    serializer_class = PostSerializer
    allowed_methods = ['GET', 'POST', 'PATCH']
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        author = self.request.user.user
        posts = Post.objects.all().filter(author=author).order_by('-published')
        return posts


class FollowRequestView(viewsets.ModelViewSet):
    """
    The api view to create a follow request
    """
    serializer_class = FollowRequestSerializer
    allowed_methods = ['GET', 'POST', 'DELETE']
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = FollowRequest.objects.all().order_by("-date_created")
            return queryset
        else:
            queryset = FollowRequest.objects.all().filter(author=self.request.user.user).order_by('-date_created')
            return queryset


@csrf_exempt
def friendrequest(request):
    user = request.user
    request.context['user'] = user

    if request.method == 'POST':
        if (user.is_authenticated):
            user = Author.objects.get(user=user)

            processed_hostname = request.POST['host']
            if (processed_hostname[-1] == '/'):
                processed_hostname = processed_hostname[:-1]

            author = {'id': str(user.id),
                      'host': user.host_url,
                      'displayName': user.username,
                      'url': user.url}
            friend = {'id': request.POST['author_id'],
                      'host': processed_hostname,
                      'displayName': request.POST['displayName'],
                      'url': request.POST['url']}
            data = {'query': 'friendrequest', 'author': json.dumps(author), 'friend': json.dumps(friend)}

            requests.post(processed_hostname + '/friendrequest', data=data)

            return HttpResponseRedirect(reverse('app:index'))
        else:
            data = request.POST

            auth = json.loads(data['author'])
            fri = json.loads(data['friend'])

            author = Author.objects.create(id=auth['id'],
                                           username=auth['displayName'],
                                           url=auth['url'],
                                           host_url=auth['host']
                                           )
            friend = Author.objects.create(id=fri['id'],
                                           username=fri['displayName'],
                                           url=fri['url'],
                                           host_url=fri['host']
                                           )

            FollowRequest.objects.create(author=author, friend=friend)

    form = AuthorForm()
    request.context['form'] = form

    return render(request, 'authors/friendrequest.html', request.context)

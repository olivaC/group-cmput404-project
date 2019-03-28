from rest_framework import viewsets
from rest_framework import permissions

from app.serializers import *
from django.http import HttpResponse, JsonResponse

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

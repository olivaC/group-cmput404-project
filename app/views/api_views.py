from rest_framework import viewsets
from app.serializers import *


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
            posts = posts.order_by('published')
            return posts

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
        queryset = Post.objects.all()
        user = self.request.user
        if user.is_staff:
            return queryset
        else:
            queryset = queryset.filter(author=user.user)
            return queryset

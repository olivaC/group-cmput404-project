from rest_framework import viewsets
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
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
def posts_by_author(request, author):
    """
    The api view to retrieve posts by author id.
    """
    if request.method == 'GET':
        print(author)
        posts = Post.objects.all().filter(author=author)
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)
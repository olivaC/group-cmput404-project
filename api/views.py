from rest_framework.generics import get_object_or_404

from api.api_utilities import *
from .serializers import *

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView


# AUTHOR API ENDPOINTS
class AuthorView(APIView):

    def get(self, request, id):
        """
        Get an author

        :param request:
        :param format:
        :return:
        """
        response = dict()

        try:
            author = get_object_or_404(Author, id=id)
            response = addAuthor(author)
            response['friends'] = addFriends(author)

            if response:
                return Response(response, status=200)
        except:
            response['author'] = []
            return Response(response, status=404)


# POSTS API ENDPOINTS
class PublicPostView(APIView):
    def get(self, request):
        response = dict()
        public = Post.objects.all().filter(visibility="PUBLIC").order_by('-published')
        response['query'] = 'posts'
        response['posts'] = postList(public)
        return Response(response, status=200)

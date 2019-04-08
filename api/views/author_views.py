from rest_framework.response import Response
from rest_framework.views import APIView

from api.api_utilities import *
from app.models import Author

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class AuthorView(APIView):
    """
    /api/author/<uuid:id>
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        """
        Get an author

        :param request:
        :param format:
        :return:
        """
        response = dict()

        try:
            author = Author.objects.get(id=id)
            response = addAuthor(author)
            response['friends'] = addFriends(author)

            if response:
                return Response(response, status=200)
        except:
            author = getRemoteAuthor(id)
            if author:
                response = author
                return Response(response, status=200)
            else:
                response['author'] = []
                return Response(response, status=404)


class AuthorListView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        /author
        Gets a list of all local authors
        """
        authors = addAuthor2()

        response = dict()

        response['author'] = authors
        response['count'] = len(authors)

        return Response(response, status=200)

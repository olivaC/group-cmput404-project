from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.api_utilities import addAuthor, addFriends
from app.models import Author


class AuthorView(APIView):
    """
    /api/author/<uuid:id>
    """

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
            author = get_object_or_404(Author, id=id)
            response = addAuthor(author)
            response['friends'] = addFriends(author)

            if response:
                return Response(response, status=200)
        except:
            response['author'] = []
            return Response(response, status=404)
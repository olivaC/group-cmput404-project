from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Author
from settings_server import DOMAIN


class FriendView(APIView):
    """
    author/<uuid:id>/friends
    """

    def get(self, request, id):
        response = dict()
        try:
            authenticated_author = request.user.user
            author = Author.objects.get(id=id)
            if author == authenticated_author:
                response['query'] = 'friends'
                response['author'] = "{}/api/{}".format(DOMAIN, authenticated_author.id)
                friends = authenticated_author.friends.all()
                friend_list = list()
                if friends:
                    for friend in friends:
                        friend_id = "{}/api/{}".format(friend.host_url, friend.id)
                        friend_list.append(friend_id)
                response['friends'] = friend_list
                return Response(response, status=200)
            else:
                raise Exception
        except:
            response['error'] = "You are not the authenticated user"
            return Response(response, status=403)


class FriendView2(APIView):
    """
    author/friends
    """

    def get(self, request):
        response = dict()
        try:
            authenticated_author = request.user.user

            response['query'] = 'friends'
            response['author'] = "{}/api/{}".format(DOMAIN, authenticated_author.id)
            friends = authenticated_author.friends.all()
            friend_list = list()
            if friends:
                for friend in friends:
                    friend_id = "{}/api/{}".format(friend.host_url, friend.id)
                    friend_list.append(friend_id)
            response['friends'] = friend_list
            return Response(response, status=200)

        except:
            response['error'] = "You are not the authenticated user"
            return Response(response, status=403)
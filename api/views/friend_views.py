from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Author, FollowRequest
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
                # response['author'] = "{}/api/author/{}".format(DOMAIN, authenticated_author.id)
                friends = authenticated_author.friends.all()
                friend_list = list()
                # if friends:
                #     for friend in friends:
                #         friend_id = "{}/api/{}".format(friend.host_url, friend.id)
                #         friend_list.append(friend_id)
                if friends:
                    for friend in friends:
                        friend_id = "{}/author/{}".format(friend.host_url, friend.id)
                        friend_list.append(friend_id)
                response['authors'] = friend_list
                return Response(response, status=200)
            else:
                raise Exception
        except:
            response['error'] = "You are not the authenticated user"
            return Response(response, status=403)


class IsFriendView(APIView):
    """
    author/<uuid:id>/friends/<uuid:id>2/
    """

    def get(self, request, id, id2):
        response = dict()
        try:
            authenticated_author = request.user.user
            author = Author.objects.get(id=id)
            potential_friend = Author.objects.get(id=id2)

            if author == authenticated_author:
                response['query'] = 'friends'
                friends = authenticated_author.friends.all()
                friend_list = list()

                if friends:
                    for friend in friends:
                        friend_list.append(friend.id)

                # check if friend
                if potential_friend.id in friend_list:
                    response['friends'] = True
                else:
                    response['friends'] = False

                authors = list()
                author_id = "{}/author/{}".format(author.host_url, author.id)
                authors.append(author_id)
                friend_id = "{}/author/{}".format(potential_friend.host_url, potential_friend.id)
                authors.append(friend_id)

                response['authors'] = authors
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
                    friend_id = "{}/api/author/{}".format(friend.host_url, friend.id)
                    friend_list.append(friend_id)
            response['friends'] = friend_list
            return Response(response, status=200)

        except:
            response['error'] = "You are not the authenticated user"
            return Response(response, status=403)


class FollowingView(APIView):
    """
    author/<uuid:id>/following
    """

    def get(self, request, id):
        response = dict()
        try:
            authenticated_author = request.user.user
            author = Author.objects.get(id=id)
            if author == authenticated_author:
                response['query'] = 'following'
                response['author'] = "{}/api/author/{}".format(DOMAIN, authenticated_author.id)
                following = FollowRequest.objects.all().filter(author=authenticated_author)

                following_list = list()
                if following:
                    for follow in following:
                        f = follow.friend
                        following_id = "{}/api/{}".format(f.host_url, f.id)
                        following_list.append(following_id)
                response['following'] = following_list
                return Response(response, status=200)
            else:
                raise Exception
        except:
            response['error'] = "You are not the authenticated user"
            return Response(response, status=403)


class FollowingView2(APIView):
    """
    author/following
    """

    def get(self, request):
        response = dict()
        try:
            authenticated_author = request.user.user
            response['query'] = 'following'
            response['author'] = "{}/api/author/{}".format(DOMAIN, authenticated_author.id)
            following = FollowRequest.objects.all().filter(author=authenticated_author)

            following_list = list()
            if following:
                for follow in following:
                    f = follow.friend
                    following_id = "{}/api/author/{}".format(f.host_url, f.id)
                    following_list.append(following_id)
            response['following'] = following_list
            return Response(response, status=200)

        except:
            response['error'] = "You are not the authenticated user"
            return Response(response, status=403)


class FollowerView(APIView):
    """
    author/<uuid:id>/followers
    """

    def get(self, request, id):
        response = dict()
        try:
            authenticated_author = request.user.user
            author = Author.objects.get(id=id)
            if author == authenticated_author:
                response['query'] = 'following'
                response['author'] = "{}/api/author/{}".format(DOMAIN, authenticated_author.id)
                followers = FollowRequest.objects.all().filter(friend=authenticated_author)

                followers_list = list()
                if followers:
                    for follow in followers:
                        f = follow.author
                        following_id = "{}/api/author/{}".format(f.host_url, f.id)
                        followers_list.append(following_id)
                response['followers'] = followers_list
                return Response(response, status=200)
            else:
                raise Exception
        except:
            response['error'] = "You are not the authenticated user"
            return Response(response, status=403)


class FollowerView2(APIView):
    """
    author/followers
    """

    def get(self, request):
        response = dict()
        try:
            authenticated_author = request.user.user

            response['query'] = 'following'
            response['author'] = "{}/api/author/{}".format(DOMAIN, authenticated_author.id)
            followers = FollowRequest.objects.all().filter(friend=authenticated_author)

            followers_list = list()
            if followers:
                for follow in followers:
                    f = follow.author
                    following_id = "{}/api/author/{}".format(f.host_url, f.id)
                    followers_list.append(following_id)
            response['followers'] = followers_list
            return Response(response, status=200)

        except:
            response['error'] = "You are not the authenticated user"
            return Response(response, status=403)

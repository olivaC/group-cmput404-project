from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import *
from api.api_utilities import *
from settings_server import DOMAIN

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class FriendView(APIView):
    """
    author/{author_id}/friends
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        response = dict()
        try:
            authenticated_author = request.user.user
            author = Author.objects.get(id=id)
            if author == authenticated_author:
                response['query'] = 'friends'
                response['author'] = "{}/api/author/{}".format(DOMAIN, authenticated_author.id)
                friends = authenticated_author.friends.all()
                friend_list = list()
                if friends:
                    for friend in friends:
                        friend_id = "{}/author/{}".format(friend.host_url, friend.id)
                        friend_list.append(friend_id)
                response['friends'] = friend_list
                response['count'] = len(friend_list)
                return Response(response, status=200)
            else:
                author = Author.objects.get(id=id)
                response['query'] = 'friends'
                response['author'] = "{}/api/author/{}".format(DOMAIN, author.id)
                friends = author.friends.all()
                friend_list = list()
                if friends:
                    for friend in friends:
                        friend_id = "{}/api/author/{}".format(friend.host_url, friend.id)
                        friend_list.append(friend_id)
                response['friends'] = friend_list
                response['count'] = len(friend_list)
                return Response(response, status=200)
        except:
            response['error'] = "You are not the authenticated user"
            return Response(response, status=403)


class FriendResponseView(APIView):
    """
    author/{author_id}/friends/
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        response = dict()

        try:
            authenticated_author = request.user.user
            author = Author.objects.get(id=id)

            response['query'] = 'friends'
            friends = authenticated_author.friends.all()
            friend_list = list()

            remote_friends = RemoteFriend.objects.all().filter(author=author)
            if remote_friends:
                for remote in remote_friends:
                    friend_list.append(remote.friend)

            if friends:
                for friend in friends:
                    friend_id = "{}/author/{}".format(friend.host_url, friend.id)
                    friend_list.append(friend_id)
            response['authors'] = friend_list

            return Response(response, status=200)

        except:
            response['error'] = "Error"
            return Response(response, status=403)


class IsFriendView(APIView):
    """
    author/<uuid:id>/friends/<uuid:id>2/
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, id, id2):
        response = dict()
        response['query'] = 'friends'
        friend_list = list()
        try:
            author = Author.objects.get(id=id)
            potential_friend = Author.objects.get(id=id2)

            friends = author.friends.all()

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

        except:
            remote_friends = RemoteFriend.objects.all().filter(author=author).first()
            if remote_friends:
                raw = remote_friends.friend
                end_id = raw.split("/")[-1]

                if end_id == str(id2):
                    response['friends'] = True
                    friend_id = remote_friends.friend

                else:
                    response['friends'] = False
                    remote_author = getRemoteAuthor(id2)
                    friend_id = remote_author.get('url')

                authors = list()
                author_id = "{}/author/{}".format(author.host_url, author.id)
                authors.append(author_id)

                authors.append(friend_id)

                response['authors'] = authors

            return Response(response, status=200)


class FriendView2(APIView):
    """
    author/friends
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

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

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

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

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

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

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

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

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

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


class FriendRequestView(APIView):
    """
    friendrequest
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        response = dict()

        f_request = FriendRequest.objects.all()
        print(f_request)
        response['query'] = 'friendrequest'

        for re in f_request:
            author_dict = dict()
            author_dict['id'] = "{}/api/author/{}".format(DOMAIN, re.author.id)
            author_dict['host'] = "{}/api/".format(re.author.host_url)
            author_dict['displayName'] = re.author.username
            author_dict['url'] = "{}/api/author/{}".format(DOMAIN, re.author.id)

            friend_dict = dict()
            friend_dict['id'] = "{}/api/author/{}".format(DOMAIN, re.friend.id)
            friend_dict['host'] = "{}/api/".format(re.friend.host_url)
            friend_dict['displayName'] = re.friend.username
            friend_dict['url'] = "{}/api/author/{}".format(DOMAIN, re.friend.id)

            response['author'] = author_dict
            response['friend'] = friend_dict

        return Response(response, status=200)

    def post(self, request):
        data = request.data
        user = request.user
        response = dict()
        response['query'] = 'friendrequest'
        try:
            friend = data.get('friend')
            author = data.get('author')
            try:
                remote = Server.objects.get(user=user)
                match = Server.objects.get(hostname=author.get('host'))
                if remote and match:
                    raw = friend.get('id')
                    uuid = raw.split('/')[-1]
                    try:
                        local_author = Author.objects.get(id=uuid)
                    except:
                        response['success'] = False
                        response['message'] = 'Local user not found'
                        return Response(response, status=404)

                    try:
                        r = RemoteFriendRequest.objects.filter(friend=local_author).filter(
                            author=author.get('id')).first()
                        if r:
                            response['success'] = False
                            response['message'] = 'Pending'
                            return Response(response, status=404)
                    except:
                        print('we good')

                    try:
                        RemoteFriendRequest.objects.create(
                            author=author.get('id'),
                            friend=local_author,
                            server=match
                        )
                        response['success'] = True
                        response['message'] = 'Friend request sent'
                        return Response(response, status=200)
                    except:
                        print('remote friend request object could not be created')
            except:
                response['success'] = False
                response['message'] = 'Errors.... Fix me.'
                return Response(response, status=500)


        except:
            r = request.POST
            friend = data.get('friend')
            author = data.get('author')
            author_username = author.get('displayName')
            friend_username = friend.get('displayName')

            auth = Author.objects.filter(username=author_username).first()
            friend_model = Author.objects.filter(username=friend_username).first()

            existing = FriendRequest.objects.filter(friend=friend_model).filter(author=auth).first()

            if existing:
                response['success'] = False
                response['message'] = 'Pending'
                return Response(response, status=400)

            if friend:
                f_request = FriendRequest.objects.create(
                    friend=friend_model,
                    author=auth,
                )
                if f_request:
                    response['success'] = True
                    response['message'] = 'friend request successful'

                    return Response(response, status=200)
                else:
                    response['success'] = False
                    response['message'] = 'Error sending friend request'

                    return Response(response, status=500)
            else:
                response['success'] = False
                response['message'] = 'Missing friend'

                return Response(response, status=500)

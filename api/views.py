from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from api.api_utilities import *
from .serializers import *

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView


# AUTHOR API ENDPOINTS
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


# POSTS API ENDPOINTS
class PublicPostView(APIView):
    """
    /api/posts
    """

    def get(self, request):
        response = dict()
        public = Post.objects.all().filter(visibility="PUBLIC").order_by('-published')
        response['query'] = 'posts'
        response['posts'] = postList(public)
        return Response(response, status=200)


class AuthorVisiblePostView(APIView):
    """
    /author/posts

    For currently authenticated user
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        posts = Post.objects.all().filter(author__id__in=request.user.user.friends.all()).filter(
            visibility="FRIENDS") | Post.objects.all().filter(author__id__in=request.user.user.friends.all()).filter(
            visibility="SERVERONLY") | Post.objects.all().filter(author=user.user) | Post.objects.all().filter(
            visibility="PUBLIC")
        posts = posts.order_by('-published')
        response = dict()
        response['query'] = 'posts'
        response['posts'] = postList(posts)
        return Response(response, status=200)


class AuthorPostView(APIView):
    """
    author/<uuid:id>/posts

    All posts of an author that are visible to the currently authenticated author

    If the author is friends with the authenticated, show all their posts except for private.
    If the author is the same as the authenticated, show all currently authenticated posts.
    If the author is not friends with the authenticated, show all public posts.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        author = get_object_or_404(Author, id=id)
        current = request.user.user

        response = dict()
        friends = current.friends.all()

        if author in friends:
            posts = Post.objects.all().filter(author=author).filter(
                visibility="FRIENDS") | Post.objects.all().filter(author=author).filter(
                visibility="PUBLIC") | Post.objects.all().filter(author=author).filter(
                visibility="FOAF") | Post.objects.all().filter(author=author).filter(
                visibility="SERVERONLY")
            posts = posts.order_by('-published')
            response['query'] = 'posts'
            response['posts'] = postList(posts)
            return Response(response, status=200)
        elif author == current:
            posts = Post.objects.all().filter(author=author)
            posts = posts.order_by('-published')
            response = dict()
            response['query'] = 'posts'
            response['posts'] = postList(posts)
            return Response(response, status=200)
        else:
            posts = Post.objects.all().filter(visibility="PUBLIC")
            posts = posts.order_by('-published')
            response['query'] = 'posts'
            response['posts'] = postList(posts)
            return Response(response, status=200)


class SinglePostView(APIView):
    """
    posts/<uuid:id>

    """

    def get(self, request, id):
        authenticated_author = request.user.user
        response = dict()
        response['query'] = 'posts'

        post = Post.objects.all().filter(id=id).first()

        if not post:
            return Response(response, status=404)

        author = post.author
        friends = author.friends.all()

        if authenticated_author in friends:
            response['posts'] = postCreate(post)
            return Response(response, status=200)
        elif post.visibility == "PUBLIC":
            response['posts'] = postCreate(post)
            return Response(response, status=200)
        elif post.author == authenticated_author:
            response['posts'] = postCreate(post)
            return Response(response, status=200)
        else:
            response['Error'] = 'Not authorized to see this post'
            return Response(response, status=403)


class CommentsView(APIView):
    """
    /posts/<uuid:id>/comments
    """

    def get(self, request, id):
        authenticated_author = request.user.user
        response = dict()
        response['query'] = 'comments'

        post = Post.objects.all().filter(id=id).first()

        if not post:
            response['Error'] = 'Post does not exist'
            return Response(response, status=404)

        author = post.author
        friends = author.friends.all()

        if authenticated_author in friends:
            response['comments'] = commentList(post)
            return Response(response, status=200)
        elif post.visibility == "PUBLIC":
            response['comments'] = commentList(post)
            return Response(response, status=200)
        elif post.author == authenticated_author:
            response['comments'] = commentList(post)
            return Response(response, status=200)
        else:
            response['Error'] = 'Not authorized to see comments of this post'
            return Response(response, status=403)


class FriendView(APIView):
    """
    author/<uuid:id>/friends
    """

    def get(self, request, id):
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

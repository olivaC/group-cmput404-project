from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from api.api_utilities import postList, postCreate
from app.models import Post, Author, Server


# https://stackoverflow.com/questions/715417/converting-from-a-string-to-boolean-in-python
def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


class PublicPostView(APIView):
    """
    /api/posts
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        response = dict()
        public = Post.objects.all().filter(visibility="PUBLIC").order_by('-published')
        response['query'] = 'posts'
        response['posts'] = postList(public)
        response['count'] = len(public)
        return Response(response, status=200)

    def post(self, request):
        user = request.user
        response = dict()
        try:
            remote = Server.objects.get(user=user)
            if remote:
                response['query'] = 'addPost'
                response['success'] = False
                response['message'] = 'Not authorized to create posts'
                return Response(response, status=403)
            else:
                response['query'] = 'addPost'
                response['success'] = False
                response['message'] = 'Not authorized to create posts'
                return Response(response, status=403)
        except:
            author = user.user
            r = request.POST
            title = r.get('title')
            description = r.get('description')
            visibility = r.get('visibility')
            content = r.get('content')
            contentType = r.get('contentType')
            unlisted = str2bool(r.get('unlisted'))

            if title and description and visibility and content and contentType and (unlisted in [True, False]):
                post = Post.objects.create(
                    author=author, title=title, description=description, visibility=visibility, content=content,
                    contentType=contentType, unlisted=bool(unlisted)
                )
                if post:
                    response['query'] = 'addPost'
                    response['success'] = True
                    response['message'] = 'Post added'

                    return Response(response, status=200)
                else:
                    response['query'] = 'addPost'
                    response['success'] = False
                    response['message'] = 'Post failed to create'

                    return Response(response, status=500)

        print('yar')


class AuthorVisiblePostView(APIView):
    """
    /author/posts

    For currently authenticated user
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        remote_id = request.META.get('HTTP_X_AUTHOR_ID')
        if remote_id:
            server = Server.objects.get(user=request.user)
            if server:
                # TODO: Filter more posts based on friends
                posts = Post.objects.all().filter(visibility="PUBLIC").order_by('-published')
        else:
            user = request.user
            posts = Post.objects.all().filter(author__id__in=request.user.user.friends.all()).filter(
                visibility="FRIENDS") | Post.objects.all().filter(
                author__id__in=request.user.user.friends.all()).filter(
                visibility="SERVERONLY") | Post.objects.all().filter(author=user.user) | Post.objects.all().filter(
                visibility="PUBLIC")
            posts = posts.order_by('-published')
        response = dict()
        response['query'] = 'posts'
        response['count'] = len(posts)
        response['posts'] = postList(posts)
        return Response(response, status=200)


# class AuthorPostView(APIView):
#     """
#     author/<uuid:id>/posts
#
#     All posts of an author that are visible to the currently authenticated author
#
#     If the author is friends with the authenticated, show all their posts except for private.
#     If the author is the same as the authenticated, show all currently authenticated posts.
#     If the author is not friends with the authenticated, show all public posts.
#     """
#
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request, id):
#         author = get_object_or_404(Author, id=id)
#         current = request.user.user
#
#         response = dict()
#         friends = current.friends.all()
#
#         if author in friends:
#             posts = Post.objects.all().filter(author=author).filter(
#                 visibility="FRIENDS") | Post.objects.all().filter(author=author).filter(
#                 visibility="PUBLIC") | Post.objects.all().filter(author=author).filter(
#                 visibility="FOAF") | Post.objects.all().filter(author=author).filter(
#                 visibility="SERVERONLY")
#             posts = posts.order_by('-published')
#             response['query'] = 'posts'
#             response['posts'] = postList(posts)
#             return Response(response, status=200)
#         elif author == current:
#             posts = Post.objects.all().filter(author=author)
#             posts = posts.order_by('-published')
#             response = dict()
#             response['query'] = 'posts'
#             response['posts'] = postList(posts)
#             return Response(response, status=200)
#         else:
#             posts = Post.objects.all().filter(visibility="PUBLIC")
#             posts = posts.order_by('-published')
#             response['query'] = 'posts'
#             response['posts'] = postList(posts)
#             return Response(response, status=200)

class AuthorPostView(APIView):
    """
    author/<uuid:id>/posts

    All posts made by {AUTHOR_ID} visible to the currently authenticated user
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        author = get_object_or_404(Author, id=id)
        current = request.user.user

        response = dict()
        friends = current.friends.all()

        # posts = Post.objects.all().filter(author=author).filter(
        #             visibility="FRIENDS") | Post.objects.all().filter(author=author).filter(
        #             visibility="PUBLIC") | Post.objects.all().filter(author=author).filter(
        #             visibility="FOAF") | Post.objects.all().filter(author=author).filter(
        #             visibility="SERVERONLY")
        #
        # posts = posts.order_by('-published')
        # response['query'] = 'posts'
        # response['posts'] = postList(posts)
        # return Response(response, status=200)

        if author in friends:
            posts = Post.objects.all().filter(author=author).filter(
                visibility="FRIENDS") | Post.objects.all().filter(author=author).filter(
                visibility="PUBLIC") | Post.objects.all().filter(author=author).filter(
                visibility="FOAF") | Post.objects.all().filter(author=author).filter(
                visibility="SERVERONLY")
            posts = posts.order_by('-published')
            response['query'] = 'posts'
            response['posts'] = postList(posts)
            response['count'] = len(posts)
            return Response(response, status=200)
        elif author == current:
            posts = Post.objects.all().filter(author=author)
            posts = posts.order_by('-published')
            response = dict()
            response['count'] = len(posts)
            response['query'] = 'posts'
            response['posts'] = postList(posts)
            return Response(response, status=200)
        else:
            posts = Post.objects.all().filter(visibility="PUBLIC")
            posts = posts.order_by('-published')
            response['count'] = len(posts)
            response['query'] = 'posts'
            response['posts'] = postList(posts)
            return Response(response, status=200)


class SinglePostView(APIView):
    """
    posts/<uuid:id>

    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

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

from rest_framework.response import Response
from rest_framework.views import APIView

from api.api_utilities import commentList
from app.models import Post

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class CommentsView(APIView):
    """
    /posts/<uuid:id>/comments
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

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
            response['count'] = len(commentList(post))
            return Response(response, status=200)
        elif post.visibility == "PUBLIC":
            response['comments'] = commentList(post)
            response['count'] = len(commentList(post))
            return Response(response, status=200)
        elif post.author == authenticated_author:
            response['comments'] = commentList(post)
            response['count'] = len(commentList(post))
            return Response(response, status=200)
        else:
            response['Error'] = 'Not authorized to see comments of this post'
            return Response(response, status=403)

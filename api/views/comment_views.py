import requests
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from api.api_utilities import commentList, getRemotePost, getRemoteComments
from app.models import Post, Server, RemoteComment

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from settings_server import DOMAIN


class CommentsView(APIView):
    """
    /posts/<uuid:id>/comments
    """

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def get(self, request, id):
        authenticated_author = request.user
        response = dict()
        response['query'] = 'comments'
        comments = None
        post_check = False

        try:
            post = Post.objects.get(id=id)
            post_check = True
        except:
            comments = getRemoteComments(id)

        if not post_check and not comments:
            response['Error'] = 'Post does not exist'
            return Response(response, status=404)
        elif comments:
            c = self.paginate_queryset(comments)
            if c is not None:
                c = self.get_paginated_response(c)
            dat = c.data
            response['comments'] = dat.get('results')
            response['previous'] = dat.get('previous')
            response['next'] = dat.get('next')
            response['count'] = dat.get('count')
            return Response(response, status=200)

        author = post.author
        friends = author.friends.all()

        if authenticated_author in friends or post.visibility == "PUBLIC" or post.author == authenticated_author:
            c = self.paginate_queryset(commentList(post))
            if c is not None:
                c = self.get_paginated_response(c)
            dat = c.data
            response['comments'] = dat.get('results')
            response['previous'] = dat.get('previous')
            response['next'] = dat.get('next')
            response['count'] = dat.get('count')
            return Response(response, status=200)
        else:
            response['Error'] = 'Not authorized to see comments of this post'
            return Response(response, status=403)

    def post(self, request, id):
        req = request.data
        post_url = req.get('post')
        comment = req.get('comment')
        author = comment.get('author')
        response = dict()
        response['query'] = 'addComment'
        s = None
        if DOMAIN in post_url:
            # Local post, do crap
            pass
        else:
            try:
                servers = Server.objects.all()
                for server in servers:
                    if server.hostname in post_url:
                        s = server
            except:
                print("server not found")

            if s:
                post = requests.get(post_url, auth=(s.username, s.password))
                if post.status_code == 200:
                    p = post.json()
                    p = p.get('posts')
                    p_id = p[0].get('id')

                    try:
                        local_post = Post.objects.get(id=p_id)
                        RemoteComment.objects.create(
                            id=p_id,
                            post=local_post,
                            server=s,
                            author=author.get('id'),
                            comment=comment.get('comment'),
                            contentType=comment.get('contentType'),
                            published=comment.get('published')
                        )
                        response['success'] = True
                        response['message'] = 'Comment Added'
                        return Response(response, status=200)
                    except:
                        response['success'] = False
                        response['message'] = 'Post could not be found'
                        return Response(response, status=404)

                else:
                    response['success'] = False
                    response['message'] = 'Post could not be found'
                    return Response(response, status=404)

            else:
                response['success'] = False
                response['message'] = "Comment not allowed"
                return Response(response, status=403)

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

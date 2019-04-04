from django.contrib.auth.decorators import login_required
from django.urls import path, include
from rest_framework import routers

import api.views as views
import api.views.author_views
import api.views.comment_views
import api.views.friend_views
import api.views.post_views

app_name = 'api'

from rest_framework_swagger.views import get_swagger_view

# Taken from https://django-rest-swagger.readthedocs.io/en/latest/
schema_view = get_swagger_view(title='Group 10 Social Distribution Remote API')

urlpatterns = [
    path('', schema_view),
    # Author
    path('author/<uuid:id>', api.views.author_views.AuthorView.as_view(), name='author'),
    path('author/', api.views.author_views.AuthorListView.as_view(), name='author_list'),

    # Posts
    path('posts', api.views.post_views.PublicPostView.as_view(), name='public'),
    path('author/posts', api.views.post_views.AuthorVisiblePostView.as_view(), name='author_visible'),
    path('author-mutual/posts', api.views.post_views.AuthorMutualPostView.as_view(), name='author_mutual_visible'),
    path('author/<uuid:id>/posts', api.views.post_views.AuthorPostView.as_view(), name='author_posts'),
    path('posts/<uuid:id>', api.views.post_views.SinglePostView.as_view(), name='single_post'),

    # Comments
    path('posts/<uuid:id>/comments', api.views.comment_views.CommentsView.as_view(), name='comments'),

    # Friends
    #path('author/<uuid:id>/friends', api.views.friend_views.FriendView.as_view(), name='friends'),
    path('author/<uuid:id>/friends/', api.views.friend_views.FriendResponseView.as_view(), name='friends'),
    path('author/<uuid:id>/friends/<uuid:id2>', api.views.friend_views.IsFriendView.as_view(), name='is_friend'),
    path('author/friends', api.views.friend_views.FriendView2.as_view(), name='friends2'),
    path('author/<uuid:id>/following', api.views.friend_views.FollowingView.as_view(), name='following'),
    path('author/following', api.views.friend_views.FollowingView2.as_view(), name='following2'),
    path('author/<uuid:id>/followers', api.views.friend_views.FollowerView.as_view(), name='followers'),
    path('author/followers', api.views.friend_views.FollowerView2.as_view(), name='followers2'),

    # Friendrequest
    path('friendrequest', api.views.friend_views.FriendRequestView.as_view(), name='friendrequest'),

]

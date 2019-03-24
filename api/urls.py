from django.urls import path

import api.views as views

app_name = 'api'

urlpatterns = [
    path('author/<uuid:id>', views.AuthorView.as_view(), name='author'),
    path('posts', views.PublicPostView.as_view(), name='public'),
    path('author/posts', views.AuthorVisiblePostView.as_view(), name='author_visible'),
    path('author/<uuid:id>/posts', views.AuthorPostView.as_view(), name='author_posts'),
    path('posts/<uuid:id>', views.SinglePostView.as_view(), name='single_post'),
    path('posts/<uuid:id>/comments', views.CommentsView.as_view(), name='comments'),
    path('author/<uuid:id>/friends', views.FriendView.as_view(), name='friends'),
]

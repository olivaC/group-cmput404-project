from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

import app.views.post_views
import app.views.user_views
from app.views import api_views, views, post_views, user_views

app_name = 'app'

# router = routers.DefaultRouter()
# router.register('author', api_views.AuthorView)
# router.register('users', api_views.UserView)
# router.register('posts', api_views.PostView, base_name='posts')
# router.register('author-posts', api_views.AuthorPostView, base_name='author_posts')
# router.register('follow-request', api_views.FollowRequestView, base_name="follow_request")

urlpatterns = [
    path('api_test', views.api_test, name='api_test'),
    # path('api/', include(router.urls)),
    path('', views.index),
    path('index', views.index, name="index"),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout', views.logout_view, name="logout"),
    path('register', views.register_view, name="register"),
    path('create-image', app.views.post_views.create_image_view, name="create_image"),
    path('images/<str:filename>', views.get_image, name="images"),
    path('images/<str:filename>/<str:encoding>', views.get_image, name="images"),
    path('my-posts', app.views.post_views.my_posts_view, name="my_posts"),
    path('create-post', app.views.post_views.create_post_view, name='create_post'),
    path('delete/<uuid:id>/', app.views.post_views.delete_post, name="delete"),
    path('author/<uuid:id>', views.profile_view, name="profile"),
    path('profile', views.my_profile_view, name="my_profile"),
    path('profile/edit/', views.edit_profile, name="edit_profile"),
    path('post/edit/<uuid:id>/', post_views.edit_post, name="edit_post"),
    path('authors', user_views.all_author_view, name="all_authors"),
    path('authors/follow/<uuid:id>/', user_views.follow_view, name="follow"),
    # path('followers/follow/<uuid:id>/', user_views.follow_view, name="followers_follow"),
    path('authors/unfollow/<uuid:id>/', user_views.unfollow_view, name="unfollow"),
    path('authors/unfollow-mutual/<uuid:id>/', user_views.unfollow_mutual_view, name="unfollow_mutual"),
    path('public-posts', app.views.post_views.public_post_view, name="public_posts"),
    path('search/', views.search_view, name="search_author"),
    path('new_followers/', user_views.new_followers_view, name="new_followers"),
    path('followers/', user_views.all_followers_view, name="followers"),

    path('mutual-friends/', user_views.mutual_friends_view, name="mutual_friends"),
    path('post-detail/<uuid:id>/', post_views.create_comment_view, name="post_detail"),
    path('foaf-posts', post_views.foaf_posts_view, name="foaf_posts"),
    path('mutual-friend-posts', post_views.mutual_friends_posts_view, name="mutual_friend_posts"),
    path('post/<uuid:id>/', post_views.unlisted_post_view, name="unlisted_post"),

    path('author/remote/', app.views.user_views.profile_remote_view, name="author_remote"),
    path('post-detail/remote/<str:post>', post_views.remote_post_view, name="remote_post"),

    path('friend-request/send/<uuid:id>',user_views.send_friend_request, name='add_friend'),
    path('friend-request/cancel/<uuid:id>',user_views.cancel_friend_request, name='cancel_friend'),
    path('friend-request/accept/<uuid:id>',user_views.accept_friend_request, name='accept_friend'),
    path('friendrequest', user_views.all_requests_view, name="requests"),

    path('remote-friend-request/accept/',user_views.accept_remote_friend_request, name='accept_remote_friend'),
    path('remote-friend-request/send/<str:uuid>',user_views.send_remote_friend_request, name='add_remote_friend'),
    path('unfollow-remote-mutual/<str:uuid>', user_views.unfriend_remote_mutual_view, name="unfriend_remote_mutual"),

    #path('friendrequest', api_views.friendrequest, name="friendrequest"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

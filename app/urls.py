from django.urls import path, include
from rest_framework import routers

import app.views.post_views
from app.views import api_views, views, post_views, user_views

app_name = 'app'

router = routers.DefaultRouter()
router.register('author', api_views.AuthorView)
router.register('users', api_views.UserView)
router.register('posts', api_views.PostView, base_name='posts')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.index),
    path('index', views.index, name="index"),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout', views.logout_view, name="logout"),
    path('register', views.register_view, name="register"),
    path('uploadimage', views.upload_image_view, name="uploadimage"),
    path('images/<str:username>/<str:filename>/<str:encoding>', views.get_image, name="images"),
    path('my-posts', app.views.post_views.my_posts_view, name="my_posts"),
    path('create-post', app.views.post_views.create_post_view, name='create_post'),
    path('delete/<uuid:id>/', app.views.post_views.delete_post, name="delete"),
    path('author/<uuid:id>', views.profile_view, name="profile"),
    path('profile/edit/', views.edit_profile, name="edit_profile"),
    path('post/edit/<uuid:id>/', post_views.edit_post, name="edit_post"),
    path('authors', user_views.all_author_view, name="all_authors"),
    path('authors/follow/<uuid:id>/', user_views.follow_view, name="follow"),
    path('authors/unfollow/<uuid:id>/', user_views.unfollow_view, name="unfollow"),
    path('authors/unfollow-mutual/<uuid:id>/', user_views.unfollow_mutual_view, name="unfollow_mutual"),
    path('public-posts', app.views.post_views.public_post_view, name="public_posts"),
    path('search/', views.search_view, name="search_author"),
    path('new_followers/', user_views.new_followers_view, name="new_followers"),
    path('followers/', user_views.all_followers_view, name="followers"),
    path('following/', user_views.all_following_view, name="following"),
    path('mutual-friends/', user_views.mutual_friends_view, name="mutual_friends"),
]

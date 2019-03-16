from django.urls import path, include
from rest_framework import routers

import app.views.post_views
from app.views import api_views, views, post_views
from django.conf.urls import url

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
    url(r'^delete/(?P<id>\d+)/$', app.views.post_views.delete_post, name="delete"),
    path('profile', views.profile_view, name="profile"),
    path('profile/edit/', views.edit_profile, name="edit_profile"),
    path('post/edit/<int:id>/', post_views.edit_post, name="edit_post"),
    path('public-posts', app.views.post_views.public_post_view, name="public_posts")
]

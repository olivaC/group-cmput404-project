from django.urls import path, include
from rest_framework import routers
from app.views import api_views, views
from django.conf.urls import url

app_name = 'app'

router = routers.DefaultRouter()
router.register('author', api_views.AuthorView)
router.register('users', api_views.UserView)
router.register('posts', api_views.PostView)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.index),
    path('index', views.index, name="index"),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout', views.logout_view, name="logout"),
    path('register', views.register_view, name="register"),
    path('my-posts', views.my_posts_view, name="myposts"),
    url(r'^delete/(?P<id>\d+)/$', views.delete_post, name="delete")
]

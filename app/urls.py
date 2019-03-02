from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from app.views import api_views,views
from SocialDistribution import settings


app_name = 'app'

router = routers.DefaultRouter()
router.register('author', api_views.AuthorView)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.index),
    path('index', views.index, name="index"),
]
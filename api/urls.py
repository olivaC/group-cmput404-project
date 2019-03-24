from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

import api.views as views

app_name = 'api'

urlpatterns = [
    path('author/<uuid:id>', views.AuthorView.as_view(), name='author'),
    path('posts', views.PublicPostView.as_view(), name='public'),
]

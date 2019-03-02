from django.urls import path, include
from rest_framework import routers
from app.views import api_views, views

app_name = 'app'

router = routers.DefaultRouter()
router.register('author', api_views.AuthorView)
router.register('users', api_views.UserView)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.index),
    path('index', views.index, name="index"),
]

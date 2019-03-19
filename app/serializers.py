from rest_framework import serializers
from app.models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')


class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = (
            'id',
            'url',
            'username',
            'bio',
            'host_url',
            'github_url',
            'friends'
        )


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'published', 'author', 'title', 'content', 'contentType', 'visibility', 'unlisted')
        depth = 1

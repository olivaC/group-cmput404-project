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
            'username',
            'description',
            'host_url',
            'github_url',
            'user',
        )
        depth = 2

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


class FollowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowRequest
        fields = ('id',
                  'author',
                  'friend')

    def create(self, validated_data):
        if validated_data.get('author'):
            author = validated_data.get('author')
            friend = validated_data.get('friend')
            FollowRequest.objects.create(
                author=author,
                friend=friend
            )
            auth_follow = FollowRequest.objects.all().filter(friend=author).filter(author=friend)
            if auth_follow:
                author.friends.add(friend)
                author.save()

from rest_framework import serializers


class AuthorSerializers(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    description = serializers.CharField(source='user.description')
    host_url = serializers.URLField(source='user.host_url')
    github_url = serializers.CharField(source='user.github_url')

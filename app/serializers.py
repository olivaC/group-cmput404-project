from rest_framework import serializers
from app.models import *


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

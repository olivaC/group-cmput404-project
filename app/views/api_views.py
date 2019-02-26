from rest_framework import viewsets
from app.models import Author
from app.serializers import *


class AuthorView(viewsets.ModelViewSet):
    """
    The api view to retrieve author.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers
    allowed_methods = ["GET"]

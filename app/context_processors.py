from django.contrib.auth.decorators import login_required

from app.models import *


def add_variable_to_context(request):
    x = request
    if request.user.is_authenticated:
        author = request.user.user
        requests = FollowRequest.objects.all().filter(friend=author).filter(acknowledged=False)
        request_len = len(list(requests))
        return {
            'requests': requests,
            'request_len': request_len
        }
    return {
        'requests': None,
        'request_len': None
    }

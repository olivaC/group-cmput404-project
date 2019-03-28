from django.contrib import admin

from app.models import *

admin.site.register(Author)
admin.site.register(FollowRequest)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Server)

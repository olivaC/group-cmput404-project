from django.contrib import admin

from app.models import *

admin.site.register(Author)
admin.site.register(FriendRequest)
admin.site.register(Friend)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Server)

import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from settings_server import *
from django.forms import ModelForm


class Author(models.Model):
    """
    user: a local user using the Django User
    username: username from either a local user or remote
    host_url: host url
    github_url: optional github url from an author
    """
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE, blank=True, null=True)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    host_url = models.URLField(blank=True, null=True)  # Url of different hosts
    github_url = models.CharField(max_length=100, blank=True, null=True)  # Optional
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    url = models.CharField(max_length=150, blank=True, null=True)
    friends = models.ManyToManyField("self", blank=True, related_name='author_friends')

    @property
    def full_name(self):
        if self.user:
            return self.user.get_full_name()

    def __str__(self):
        return "{} - {}".format(str(self.username), self.host_url)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        self.url = "{}/author/{}".format(self.host_url, self.id)
        super(self.__class__, self).save(*args, **kwargs)


class FriendRequest(models.Model):
    """
    Friend class, status will indicate whether a request was rejected or accepted.

    Example: Author A and Author B;

    A friend requests B --> FR = FriendRequest()
    A is following B
        1) Check if B exists as a requester
        2) If B exists as a requester, check if A is requestee, check if A already accepted a friend request
        3) If A already accepted a friend request, create a Friend object
    """
    requester = models.ForeignKey(Author, related_name='requester', on_delete=models.CASCADE)
    requestee = models.ForeignKey(Author, related_name='requestee', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    acknowledged = models.BooleanField(default=False)

    def __str__(self):
        return "{} to {} on {}".format(self.requester, self.requestee, self.date_created)

    def save(self, *args, **kwargs):
        super(self.__class__, self).save(*args, **kwargs)

        # Check and make a Friend model
        requester_models = FriendRequest.objects.filter(requester=self.requestee).filter(acknowledged=True).filter(
            status=True)
        if requester_models:
            Friend.objects.create(friend1=self.requester, friend2=self.requestee)


class Friend(models.Model):
    """
    Only create by checking FriendRequest.
    """
    friend1 = models.ForeignKey(Author, related_name='friend1', on_delete=models.CASCADE)
    friend2 = models.ForeignKey(Author, related_name='friend2', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.friend1.username, self.friend2.username)


POST_PRIVACY = (
    ('Private', 'PRIVATE'),
    ('All friends on my host', 'SERVERONLY'),
    ('All friends', 'FRIENDS'),
    ('My friends friends', 'FOAF'),
    ('Public', 'PUBLIC'),
)

POST_CONTENT_TYPE = (
    ('Plain Text', 'text/plain'),
    ('Markdown', 'text/markdown')
)


class Post(models.Model):
    # TODO: Finish this class
    author = models.ForeignKey(Author, related_name='authorPost', on_delete=models.CASCADE)
    published = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)  # brief description
    visibility = models.CharField(max_length=100, choices=POST_PRIVACY, default='Private')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    content = models.TextField(default="")
    contentType = models.CharField(max_length=100, choices=POST_CONTENT_TYPE, default='Plain Text')
    unlisted = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {} - {}".format(self.author, self.published, self.visibility)

    def __repr__(self):
        return "{} - {} - {}".format(self.author, self.published, self.visibility)


class Image(models.Model):
    def get_image_dir(instance, filename):
        if isinstance(instance, str):
            return "images/{username}/{filename}".format(username=instance, filename=filename)
        else:
            authorName = instance.author.username
            return Image.get_image_dir(authorName, filename)

    author = models.ForeignKey(Author, related_name='authorImage', on_delete=models.CASCADE)
    private = models.IntegerField(default=0)
    file = models.FileField(upload_to=get_image_dir)


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ["file", "private"]


class Comment(models.Model):
    # TODO: Finish this class
    pass


class Server(models.Model):
    # TODO: Finish this class
    pass


@receiver(post_save, sender=User)
def create_user_author(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance, host_url=DOMAIN)
        instance.user.author_id = uuid.uuid4()
        instance.user.url = "{}/author/{}".format(instance.user.host_url, instance.user.author_id)
        instance.user.username = instance.username
        instance.user.save()

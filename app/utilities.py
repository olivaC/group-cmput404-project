import mimetypes
import urllib.parse
from datetime import datetime

from django.utils.safestring import mark_safe
from PIL import Image
from io import BytesIO
import base64

from pytz import utc

from app.models import Author, Post, Comment


def unquote_redirect_url(url):
    """
    Unquotes url

    :param url:
    :return:
    """
    url = urllib.parse.unquote(url)
    if url.endswith("/") and not url == '/':
        return url[:-1]
    return url



def api_check(user):
    if 'frandzone' in user.username or 'testApi' in user.username:
        return False
    else:
        return True


def image_posts_to_html(posts):
    for post in posts:
        image_post_to_html(post)


def image_post_to_html(post):
    print(post.contentType)
    if post.contentType.startswith("image/"):
        post.content = image_content_to_html(post.content)


def image_content_to_html(content):
    return mark_safe("<img src=\"" + content + "\" />")


def get_image_type(fileName):
    if fileName.endswith(".jpg"):
        return "image/jpeg"
    elif fileName.endswith(".png"):
        return "image/png"


def get_base64(mimeType, file):
    data = "data:" + mimeType + ";base64," + base64.b64encode(file.read()).decode("utf-8")
    return data


def get_image_from_base64(base64String):
    return base64.b64decode(base64String)



def create_author(author):
    i = Author()
    if not author.get('displayName'):
        i.username = author.get('id')
    else:
        i.username = author.get('displayName')
    i.host_url = author.get('host')
    i.id = author.get('id')
    i.uuid = i.id.split("/")[-1]
    i.url = author.get('url')
    if author.get('firstName'):
        i.first_name = author.get('firstName')
    if author.get('lastName'):
        i.last_name = author.get('lastName')
    return i


def create_posts(posts):
    post_list = list()

    for i in posts.get('posts'):
        post = Post()
        post.id = i.get('id')
        post.author = create_author(i.get('author'))
        post.contentType = i.get('contentType')
        post.description = i.get('description')
        post.published = utc.localize(datetime.strptime(i.get('published'), '%Y-%m-%dT%H:%M:%S.%fZ'))
        post.unlisted = i.get('unlisted')
        post.visibility = i.get('visibility')
        post.title = i.get('title')
        post.remote = 'remote'
        post.content = i.get('content')
        post.content = post.get_content()
        post_list.append(post)

    return post_list


def create_post(i):
    post = Post()
    post.id = i.get('id')
    post.author = create_author(i.get('author'))
    post.contentType = i.get('contentType')
    post.description = i.get('description')
    post.published = utc.localize(datetime.strptime(i.get('published'), '%Y-%m-%dT%H:%M:%S.%fZ'))
    post.unlisted = i.get('unlisted')
    post.visibility = i.get('visibility')
    post.title = i.get('title')
    post.remote = 'remote'
    post.content = i.get('content')
    post.content = post.get_content()

    return post


def create_comments(post):
    comment_list = list()
    for c in post.get('comments'):
        comment = Comment()
        comment.author = create_author(c.get('author'))
        comment.comment = c.get('comment')
        comment.contentType = c.get('contentType')
        comment.content = comment.get_comment()
        comment.id = c.get('id')
        comment.published = utc.localize(datetime.strptime(c.get('published'), '%Y-%m-%dT%H:%M:%S.%fZ'))
        comment_list.append(comment)
    return comment_list

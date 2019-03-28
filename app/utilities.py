import urllib.parse
<<<<<<< HEAD

from app.models import Server

=======
from django.utils.safestring import mark_safe
from PIL import Image
from io import BytesIO
import base64
>>>>>>> d6bb207b33bb19541c1adefb292618c2d4b05404

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

<<<<<<< HEAD

def api_check(user):

    if 'group10api' in user.username:
        return False
    else:
        return True
=======
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
>>>>>>> d6bb207b33bb19541c1adefb292618c2d4b05404

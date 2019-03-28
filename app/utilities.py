import mimetypes
import urllib.parse
from django.utils.safestring import mark_safe
from PIL import Image
from io import BytesIO
import base64


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


def image_posts_to_html(posts):
    for post in posts:
        image_post_to_html(post)


def image_post_to_html(post):
    print(post.contentType)
    if post.contentType.startswith("image/"):
        post.content = image_content_to_html(post.content)


def image_content_to_html(content):
    return mark_safe("<img src=\"" + content + "\" />")


def get_image(file):
    p = Image.open(file)
    p = p.convert('RGB')
    buffered = BytesIO()
    p.save(buffered, format="JPEG", quality=30, optimize=True)
    encoded_picture = str(base64.b64encode(buffered.getvalue()), 'utf-8')
    img_str = "data:img/png;base64,"
    return "{}{}".format(img_str, encoded_picture)

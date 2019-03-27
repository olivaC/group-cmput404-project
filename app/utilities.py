import urllib.parse
from django.utils.safestring import mark_safe

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

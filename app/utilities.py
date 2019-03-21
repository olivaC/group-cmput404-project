import urllib.parse


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

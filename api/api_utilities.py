import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from app.models import Comment, Author, Server
from settings_server import DOMAIN
from datetime import datetime
from pytz import utc
from itertools import groupby



def addAuthor(author):
    """
    Creates an Author dictionary

    :param author: Author instance
    :return: Dict
    """
    author_dict = dict()
    # author_dict['id'] = "{}/api/{}".format(DOMAIN, author.id)
    author_dict['id'] = "{}/api/author/{}".format(DOMAIN, author.id)
    author_dict['host'] = "{}/api/".format(author.host_url)
    author_dict['displayName'] = author.username
    author_dict['github'] = author.github_url
    author_dict['url'] = "{}/api/author/{}".format(DOMAIN, author.id)

    # Optional Attributes
    if author.github_url:
        author_dict['github'] = author.github_url
    if author.user.first_name:
        author_dict['firstName'] = author.user.first_name
    if author.user.last_name:
        author_dict['lastName'] = author.user.last_name
    if author.user.email:
        author_dict['email'] = author.user.email
    if author.bio:
        author_dict['bio'] = author.bio

    return author_dict


def remoteAddAuthor(author):
    """
    Creates an Author dictionary

    :param author: Author instance
    :return: Dict
    """
    author_dict = dict()
    author_dict['id'] = author.get('id')
    author_dict['host'] = author.get('host')
    author_dict['displayName'] = author.get('displayName')
    author_dict['github'] = author.get('github')
    author_dict['url'] = author.get('url')

    # Optional Attributes
    if author.get('github_url'):
        author_dict['github'] = author.get('github_url')
    if author.get('firstName'):
        author_dict['firstName'] = author.get('firstName')
    if author.get('lastName'):
        author_dict['lastName'] = author.get('lastName')
    if author.get('email'):
        author_dict['email'] = author.get('email')
    if author.get('bio'):
        author_dict['bio'] = author.get('bio')

    return author_dict


def addAuthor2():
    """
    Creates an Author dictionary

    :param author: Author instance
    :return: List
    """

    author_list = list()

    authors = Author.objects.all()

    for author in authors:
        author_dict = dict()
        author_dict['id'] = "{}/api/author/{}".format(DOMAIN, author.id)
        author_dict['host'] = "{}/api/".format(author.host_url)
        author_dict['displayName'] = author.username
        author_dict['url'] = "{}/api/author/{}".format(DOMAIN, author.id)

        author_list.append(author_dict)

    return author_list


def addFriends(author):
    friends = author.friends.all()
    friend_list = list()
    if friends:
        for friend in friends:
            friend_dict = {'id': "{}/api/{}".format(DOMAIN, friend.id), 'host': friend.host_url,
                           'displayName': friend.username, 'url': "{}/api/{}".format(DOMAIN, friend.id)}
            friend_list.append(friend_dict)

    return friend_list


def postList(posts):
    post_list = list()
    for post in posts:
        post_dict = {'author': addAuthor(post.author), 'title': post.title, 'description': post.description,
                     'contentType': post.contentType, 'content': post.content, 'published': post.published,
                     'visibility': post.visibility, 'unlisted': post.unlisted, 'id': post.id,
                     'comments': commentList(post), 'origin': "{}/api/posts/{}".format(DOMAIN, post.id),
                     'source': "{}/api/posts/{}".format(DOMAIN, post.id)}
        post_list.append(post_dict)
    return post_list


def remoteCommentList(post):
    comments = post.get('comments')
    comment_list = list()

    if comments:
        for comment in comments:
            comment_dict = dict()
            comment_dict['author'] = remoteAddAuthor(comment.get('author'))
            comment_dict['comment'] = comment.get('comment')
            comment_dict['contentType'] = comment.get('contentType')
            comment_dict['published'] = utc.localize(
                datetime.strptime(comment.get('published'), '%Y-%m-%dT%H:%M:%S.%fZ'))
            comment_dict['id'] = comment.get('id')
            comment_list.append(comment_dict)

    comment_list = sorted(comment_list, key=lambda k: k['published'], reverse=True)

    return comment_list


def remotePostList(host, posts):
    post_list = list()
    posts = posts.get('posts')
    for post in posts:
        author = remoteAddAuthor(post.get('author'))
        title = post.get('title')
        description = post.get('description')
        contentType = post.get('contentType')
        content = post.get('content')
        published = utc.localize(datetime.strptime(post.get('published'), '%Y-%m-%dT%H:%M:%S.%fZ'))
        visibility = post.get('visibility')
        unlisted = post.get('unlisted')
        id = post.get('id')
        origin = post.get('source')
        comments = remoteCommentList(post)
        if host.endswith("/"):
            host = host[:-1]
        source = "{}/posts/{}".format(host, post.get('id'))

        post_dict = {'author': author, 'title': title, 'description': description,
                     'contentType': contentType, 'content': content, 'published': published,
                     'visibility': visibility, 'unlisted': unlisted, 'id': id,
                     'comments': comments, 'origin': origin,
                     'source': source}
        post_list.append(post_dict)
    return post_list


def remotePostCreate(host, post):
    post = post.get('posts')[0]
    author = remoteAddAuthor(post.get('author'))
    title = post.get('title')
    description = post.get('description')
    contentType = post.get('contentType')
    content = post.get('content')
    published = utc.localize(datetime.strptime(post.get('published'), '%Y-%m-%dT%H:%M:%S.%fZ'))
    visibility = post.get('visibility')
    unlisted = post.get('unlisted')
    id = post.get('id')
    origin = post.get('origin')
    comments = remoteCommentList(post)
    source = "{}/api/posts/{}".format(DOMAIN, post.get('id'))

    post_dict = {'author': author, 'title': title, 'description': description,
                 'contentType': contentType, 'content': content, 'published': published,
                 'visibility': visibility, 'unlisted': unlisted, 'id': id,
                 'comments': comments, 'origin': origin,
                 'source': source}
    return post_dict


def postCreate(post):
    post_list = list()

    post_dict = {'author': addAuthor(post.author), 'title': post.title, 'description': post.description,
                 'contentType': post.contentType, 'content': post.content, 'published': post.published,
                 'visibility': post.visibility, 'unlisted': post.unlisted, 'id': post.id,
                 'comments': commentList(post), 'source': "{}/api/posts/{}".format(DOMAIN, post.id),
                 'origin': "{}/api/posts/{}".format(DOMAIN, post.id)}
    post_list.append(post_dict)
    return post_list


def commentList(post):
    comments = Comment.objects.all().filter(post=post).order_by('-published')
    comment_list = list()

    if comments:
        for comment in comments:
            comment_dict = dict()
            comment_dict['author'] = addAuthor(comment.author)
            comment_dict['comment'] = comment.comment
            comment_dict['contentType'] = comment.contentType
            comment_dict['published'] = comment.published
            comment_dict['id'] = comment.id
            comment_list.append(comment_dict)

    return comment_list


def getRemotePost(post_id):
    servers = Server.objects.all()
    for server in servers:
        host = server.hostname
        if not host.endswith("/"):
            host = host + "/"
        server_api = "{}posts/{}".format(host, post_id)
        print('Request:')
        print(server_api)
        try:
            r = requests.get(server_api, auth=(server.username, server.password))
            print(r)
            if r.status_code in [200, 201]:
                return [remotePostCreate(server.hostname, r.json())]
        except Exception as e:
            print(e)
    return None


# https://stackoverflow.com/questions/715417/converting-from-a-string-to-boolean-in-python
def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def get_public_posts(server_posts):
    public_list = server_posts
    post = list()
    servers = Server.objects.all()

    for server in servers:
        host = server.hostname
        if not host.endswith("/"):
            host = host + "/"
        server_api = "{}posts".format(host)
        print(server.username, server.password)
        print("หำพอำพ")
        print(server_api)
        try:
            s = requests.Session()

            retries = Retry(total=5,
                            backoff_factor=0.1,
                            status_forcelist=[500, 502, 503, 504])

            s.mount('http://', HTTPAdapter(max_retries=retries))
            s.mount('https://', HTTPAdapter(max_retries=retries))

            r = s.get(server_api, auth=(server.username, server.password))

            print(r)

            if r.status_code == 200:

                posts = remotePostList(server.hostname, r.json())
                print(posts)
                # public_list.extend(posts)
                # public_list = sorted(public_list, key=lambda k: k['published'], reverse=True)
                # public_list = [next(v) for k, v in groupby(public_list, lambda d: d["id"])]

        except Exception as e:
            print(e)

    public_list.extend(posts)
    public_list = sorted(public_list, key=lambda k: k['published'], reverse=True)
    public_list = [next(v) for k, v in groupby(public_list, lambda d: d["id"])]

    return public_list

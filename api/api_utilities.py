from app.models import Comment
from settings_server import DOMAIN


def addAuthor(author):
    """
    Creates an Author dictionary

    :param author: Author instance
    :return: Dict
    """
    author_dict = dict()
    author_dict['id'] = "{}/api/{}".format(DOMAIN, author.id)
    author_dict['host'] = author.host_url
    author_dict['displayName'] = author.username
    author_dict['url'] = "{}/api/{}".format(DOMAIN, author.id)

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
                     'comments': commentList(post)}
        post_list.append(post_dict)
    return post_list


def postCreate(post):
    post_list = list()

    post_dict = {'author': addAuthor(post.author), 'title': post.title, 'description': post.description,
                 'contentType': post.contentType, 'content': post.content, 'published': post.published,
                 'visibility': post.visibility, 'unlisted': post.unlisted, 'id': post.id,
                 'comments': commentList(post)}
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

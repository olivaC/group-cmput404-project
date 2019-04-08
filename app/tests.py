import factory
from django.test import TestCase
from app.models import *
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from selenium import webdriver


class UserFactory(DjangoModelFactory):
    username = factory.Sequence('testuser{}'.format)
    email = factory.Sequence(lambda a: 'testuser{0}@404group5.com'.format)

    class Meta:
        model = User


class AuthorModelTest(TestCase):

    def setUp(self):
        user = UserFactory(username='defaultUser', email='defaultEmail')
        user.first_name = 'defaultFirst'
        user.last_name = 'defaultLast'
        user.save()

        Author.objects.create(username="RemoteAuthor", host_url="remoteurl.com")

    def test_local_author_created(self):
        user = UserFactory()
        self.assertEqual(user.user.username, 'testuser2')

    def test_local_author_full_name(self):
        author = Author.objects.get(user__email='defaultEmail')
        self.assertEqual(author.full_name, 'defaultFirst defaultLast')

    def test_local_author_description(self):
        author = Author.objects.get(user__email='defaultEmail')
        self.assertEqual(author.bio, None)

        author.bio = 'Test Description'
        author.save()

        self.assertEqual(author.bio, 'Test Description')

    def test_local_author_change_name(self):
        author = Author.objects.get(user__email='defaultEmail')

        self.assertEqual(author.full_name, 'defaultFirst defaultLast')

        author.user.first_name = 'NewFirst'
        author.user.last_name = 'NewLast'
        author.user.save()

        # Only for local authors
        self.assertEqual(author.full_name, 'NewFirst NewLast')

    def test_local_author_host_url(self):
        user1 = UserFactory()
        self.assertEqual(user1.user.host_url, DOMAIN)

    def test_local_author_github_url(self):
        user0 = UserFactory()
        user0.user.github_url = 'giturl@testgit.com'
        user0.user.save()

        self.assertEqual(user0.user.github_url, 'giturl@testgit.com')

    def test_remote_author_created(self):
        author = Author.objects.get(username="RemoteAuthor")
        self.assertEqual(author.username, 'RemoteAuthor')

    def test_remote_author_host_url(self):
        author = Author.objects.get(username="RemoteAuthor")
        self.assertEqual(author.host_url, 'remoteurl.com')

    def test_remote_author_no_user(self):
        author = Author.objects.get(username="RemoteAuthor")
        self.assertEqual(author.user, None)


class PostModelTest(TestCase):

    def setUp(self):
        user = UserFactory(username='defaultUser', email='defaultEmail')
        user.first_name = 'defaultFirst'
        user.last_name = 'defaultLast'
        user.save()

        Author.objects.create(username="RemoteAuthor", host_url="remoteurl.com")

    def test_post_local_author_exists(self):
        author = Author.objects.get(username="defaultUser")
        content = "Test post"
        contentType = "text/plain"
        title = "Test"
        description = "description"
        visibility = "PUBLIC"

        post = Post.objects.create(author=author, content=content, contentType=contentType, title=title,
                                   description=description, visibility=visibility)
        self.assertEqual(post.author, author)

    def test_post_datetime_exists(self):
        author = Author.objects.get(username="defaultUser")
        content = "Test post"
        contentType = "text/plain"
        title = "Test"
        description = "description"
        visibility = "PUBLIC"

        post = Post.objects.create(author=author, content=content, contentType=contentType, title=title,
                                   description=description, visibility=visibility)
        self.assertTrue(post.published)
        self.assertEqual(str(post.published.__class__), "<class 'datetime.datetime'>")

    def test_post_text_exists(self):
        author = Author.objects.get(username="RemoteAuthor")
        content = "Test post"
        contentType = "text/plain"
        title = "Test"
        description = "description"
        visibility = "PUBLIC"

        post = Post.objects.create(author=author, content=content, contentType=contentType, title=title,
                                   description=description, visibility=visibility)
        post.content = "Changed Text"
        post.save()
        self.assertEqual(post.content, "Changed Text")

    def test_post_private(self):
        author = Author.objects.get(username="RemoteAuthor")
        content = "Test post"
        contentType = "text/plain"
        title = "Test"
        description = "description"
        visibility = "PUBLIC"

        post = Post.objects.create(author=author, content=content, contentType=contentType, title=title,
                                   description=description, visibility=visibility)
        self.assertNotEquals(post.visibility, "PRIVATE")

    def test_post_title(self):
        author = Author.objects.get(username="RemoteAuthor")
        content = "Test post"
        contentType = "text/plain"
        title = "Test"
        description = "description"
        visibility = "PUBLIC"

        post = Post.objects.create(author=author, content=content, contentType=contentType, title=title,
                                   description=description, visibility=visibility)
        self.assertEquals(post.title, "Test")

    def test_post_multiple_exists(self):
        author = Author.objects.get(username="RemoteAuthor")
        content = "Test post"
        contentType = "text/plain"
        title = "Test"
        description = "description"
        visibility = "PUBLIC"

        Post.objects.create(author=author, content=content, contentType=contentType, title=title,
                            description=description, visibility=visibility)
        Post.objects.create(author=author, content=content, contentType=contentType, title=title,
                            description=description, visibility=visibility)

        posts = Post.objects.filter(author=author).order_by('id')
        post_len = 2
        self.assertEqual(len(posts), post_len)

    def test_post_markdown(self):
        author = Author.objects.get(username="RemoteAuthor")
        content = "Test post"
        contentType = "text/markdown"
        title = "Test"
        description = "description"
        visibility = "PUBLIC"

        post = Post.objects.create(author=author, content=content, contentType=contentType, title=title,
                                   description=description, visibility=visibility)

        self.assertEqual(post.contentType, "text/markdown")

    def test_post_unlisted(self):
        author = Author.objects.get(username="RemoteAuthor")
        content = "Test post"
        contentType = "text/markdown"
        title = "Test"
        description = "description"
        visibility = "PUBLIC"

        post = Post.objects.create(author=author, content=content, contentType=contentType, title=title,
                                   description=description, visibility=visibility, unlisted=True)

        self.assertTrue(post.unlisted)


class CommentModelTest(TestCase):

    def setUp(self):
        user = UserFactory(username='defaultUser', email='defaultEmail')
        user.first_name = 'defaultFirst'
        user.last_name = 'defaultLast'
        user.save()

        Author.objects.create(username="RemoteAuthor", host_url="remoteurl.com")

    def test_create_comment(self):
        author1 = Author.objects.get(username="RemoteAuthor")
        author2 = Author.objects.get(username="defaultUser")

        content = "Test post"
        contentType = "text/markdown"
        title = "Test"
        description = "description"
        visibility = "PUBLIC"

        post = Post.objects.create(author=author1, content=content, contentType=contentType, title=title,
                                   description=description, visibility=visibility, unlisted=True)

        com_type = "text/plain"
        com_content = "This is a test"

        comment = Comment.objects.create(post=post, author=author2, comment=com_content, contentType=com_type)

        self.assertEqual(comment.post.author, author1)
        self.assertEqual(comment.comment, "This is a test")


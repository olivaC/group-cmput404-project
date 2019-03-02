import factory
from django.test import TestCase
from app.models import *
from factory.django import DjangoModelFactory


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
        self.assertEqual(author.description, None)

        author.description = 'Test Description'
        author.save()

        self.assertEqual(author.description, 'Test Description')

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
        text = "Test post"
        post = Post.objects.create(author=author, text=text)
        self.assertEqual(post.author, author)

    def test_post_remote_author_exists(self):
        author = Author.objects.get(username="RemoteAuthor")
        text = "Test post"
        post = Post.objects.create(author=author, text=text)
        self.assertEqual(post.author, author)

    def test_post_datetime_exists(self):
        author = Author.objects.get(username="RemoteAuthor")
        text = "Test post"
        post = Post.objects.create(author=author, text=text)
        self.assertTrue(post.date_created)
        self.assertEqual(str(post.date_created.__class__), "<class 'datetime.datetime'>")

    def test_post_text_exists(self):
        author = Author.objects.get(username="RemoteAuthor")
        text = "Test post"
        post = Post.objects.create(author=author, text=text)
        self.assertEqual(post.text, text)
        post.text = "Changed Text"
        post.save()
        self.assertEqual(post.text, "Changed Text")

    def test_post_private(self):
        author = Author.objects.get(username="RemoteAuthor")
        text = "Test post"
        post = Post.objects.create(author=author, text=text)
        self.assertTrue(post.private)

    def test_post_public(self):
        author = Author.objects.get(username="RemoteAuthor")
        text = "Test post"
        post = Post.objects.create(author=author, text=text)
        self.assertTrue(post.private)

        post.private = False
        post.save()
        self.assertFalse(post.private)

    def test_post_multiple_exists(self):
        author = Author.objects.get(username="RemoteAuthor")
        text1 = "Test post 1"
        text2 = "Test post 2"
        Post.objects.create(author=author, text=text1)
        Post.objects.create(author=author, text=text2)

        posts = Post.objects.filter(author=author).order_by('id')
        post_len = 2
        self.assertEqual(len(posts), post_len)

    def test_post_multiple_delete(self):
        author = Author.objects.get(username="RemoteAuthor")
        text1 = "Test post 1"
        text2 = "Test post 2"
        Post.objects.create(author=author, text=text1)
        Post.objects.create(author=author, text=text2)

        posts = Post.objects.filter(author=author).order_by('id')
        post_len = 2
        self.assertEqual(len(posts), post_len)

        post = posts.filter(id=1)
        post.delete()

        posts = Post.objects.filter(author=author).order_by('id')

        self.assertEqual(len(posts), 1)

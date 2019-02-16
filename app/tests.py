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
        UserFactory(username='defaultUser', email='defaultEmail')

    def test_local_author_created(self):
        user1 = UserFactory()
        self.assertEqual(user1.user.username, 'testuser1')

    def test_local_author_full_name(self):
        user = User.objects.get(email='defaultEmail')
        user.first_name = 'defaultFirst'
        user.last_name = 'defaultLast'
        user.save()

        author = Author.objects.get(user__email='defaultEmail')

        self.assertEqual(user.get_full_name(), 'defaultFirst defaultLast')
        self.assertEqual(author.full_name, 'defaultFirst defaultLast')

    def test_local_author_host_url(self):
        user1 = UserFactory()
        self.assertEqual(user1.user.host_url, DOMAIN)

    def test_local_author_github_url(self):
        user0 = UserFactory()
        user0.user.github_url = 'giturl@testgit.com'
        user0.user.save()

        self.assertEqual(user0.user.github_url, 'giturl@testgit.com')

    def test_remote_author_created(self):
        # TODO: test_remote_author_created
        pass

    def test_remote_author_host_url(self):
        # TODO: test_remote_author_host_url
        pass

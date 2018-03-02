from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from ..models import Board, Topic, Post
from ..views import PostUpdateView


class PostUpdateViewTestCase(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Board', description='Board Test')
        self.username = 'johnny'
        self.password = '123'
        user = User.objects.create_user(username=self.username, email='test@test.test', password=self.password)
        self.topic = Topic.objects.create(subject='Test test', board=self.board, starter=user)
        self.post = Post.objects.create(message='Test test test', topic=self.topic, created_by=user)
        self.url = reverse('edit_post', kwargs={
            'pk': self.board.pk,
            'topic_pk': self.topic.pk,
            'post_pk': self.post.pk
            })


class LoginRequiredPostUpdateViewTests(PostUpdateViewTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{0}?next={1}'.format(login_url, self.url))


class UnauthorizedPostUpdateViewTests(PostUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        username = 'jenny'
        password = '123'
        user = User.objects.create_user(username=username, email='test2@test.test', password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 404)


class PostUpdateViewTests(PostUpdateViewTestCase):  # TODO: TESTS
    pass


class SuccessfulPostUpdateViewTests(PostUpdateViewTestCase):
    pass


class InvalidPostUpdateViewTests(PostUpdateViewTestCase):
    pass
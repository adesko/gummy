from django.test import TestCase
from django.urls import resolve, reverse
from boards.views import TopicListView
from boards.models import Board

# Create your tests here.


class BoardTopicsTests(TestCase):

    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board')

    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_home_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEqual(view.func.view_class, TopicListView)

    def test_board_topics_page_contains_navigation_links(self):
        home_page_url = reverse('home')
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        self.assertContains(response, 'href="{0}"'.format(home_page_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))
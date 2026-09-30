from django.test import TestCase

from games.models import GameProgress, MiniGame


class GameModelTests(TestCase):
    def test_game_progress_can_be_created(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.create_user(username='tester', email='tester@example.com', password='StrongPass!123')
        topic = self._make_topic('Su Bilinci')
        game = MiniGame.objects.create(title='Sayılarla Su', slug='sayilarla-su', game_type='multiple_choice', status='ready', topic=topic)
        progress = GameProgress.objects.create(user=user, game=game, status='started', attempts_count=1, score=80)
        self.assertEqual(progress.user, user)

    def test_placeholder_game_cannot_be_completed(self):
        topic = self._make_topic('Gıda Güvenliği')
        game = MiniGame.objects.create(title='Yakında', slug='yakinda', game_type='multiple_choice', status='placeholder', topic=topic)
        self.assertFalse(game.can_be_completed())

    @staticmethod
    def _make_topic(title):
        from learning.models import Topic

        return Topic.objects.create(title=title, slug=title.lower().replace(' ', '-'), is_published=True)


class GameViewTests(TestCase):
    def test_game_page_loads(self):
        from django.urls import reverse

        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)

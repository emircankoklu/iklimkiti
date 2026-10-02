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

    def test_standalone_games_appear_in_game_list_and_can_be_searched(self):
        from django.urls import reverse

        response = self.client.get(reverse('game_list'))
        self.assertContains(response, 'Gıdanı Doğru Sakla')
        self.assertContains(response, 'İsraf Dedektifi')

        response = self.client.get(reverse('game_list'), {'q': 'dedektif'})
        self.assertContains(response, 'İsraf Dedektifi')
        self.assertNotContains(response, 'Gıdanı Doğru Sakla')

    def test_standalone_games_require_login_and_render_for_authenticated_users(self):
        from django.contrib.auth import get_user_model
        from django.urls import reverse

        routes = ('food_storage_game', 'waste_detective_game')
        for route in routes:
            response = self.client.get(reverse(route))
            self.assertEqual(response.status_code, 302)

        user = get_user_model().objects.create_user(
            username='gameuser',
            password='StrongPass!123',
        )
        self.client.force_login(user)
        for route in routes:
            response = self.client.get(reverse(route))
            self.assertEqual(response.status_code, 200)

    def test_matching_game_is_not_listed(self):
        from django.urls import reverse
        topic = GameModelTests._make_topic('İklim ve Gıda')
        MiniGame.objects.create(title='Eşleştir', slug='eslestir', game_type='matching', status='ready', topic=topic)
        MiniGame.objects.create(title='İklim Bilgisi', slug='iklim-bilgisi', game_type='multiple_choice', status='ready', topic=topic)

        response = self.client.get(reverse('game_list'))
        self.assertNotContains(response, 'Eşleştir')
        self.assertContains(response, 'İklim Bilgisi')

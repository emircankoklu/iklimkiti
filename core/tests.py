from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import GuideSection, IdeathonGuide


class CoreViewTests(TestCase):
    def test_homepage_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_chatbot_fallback_when_disabled(self):
        from core.services.chatbot import GeminiChatbotService

        service = GeminiChatbotService()
        self.assertIn('yanıt veremiyor', service.get_safe_fallback_response().lower())

    def test_ideathon_guide_is_staff_only_at_admin_link(self):
        guide = IdeathonGuide.objects.create(introduction='Rehber')
        GuideSection.objects.create(
            guide=guide,
            title='Kanıt avı',
            body='Okul verisini topla.',
            order=1,
        )

        self.assertEqual(self.client.get('/cop31/').status_code, 404)
        url = '/admin/cop31-briefing-7f3c/'
        self.assertEqual(self.client.get(url).status_code, 302)

        admin = get_user_model().objects.create_superuser('admin', 'admin@example.com', 'StrongPass!123')
        self.client.force_login(admin)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Kanıt avı')
        self.assertContains(self.client.get('/admin/'), 'cop31-briefing-7f3c')

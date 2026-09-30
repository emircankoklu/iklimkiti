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

    def test_ideathon_guide_is_available(self):
        guide = IdeathonGuide.objects.create(introduction='Rehber')
        GuideSection.objects.create(
            guide=guide,
            title='Kanıt avı',
            body='Okul verisini topla.',
            order=1,
        )

        response = self.client.get('/cop31/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Kanıt avı')

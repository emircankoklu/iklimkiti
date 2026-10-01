from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from types import SimpleNamespace
from unittest.mock import patch

from core.models import ChatPromptLog, GuideSection, IdeathonGuide


class CoreViewTests(TestCase):
    def test_homepage_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'İklim Tabağım')
        self.assertContains(response, 'images/iklim-tabagim-logo.png')
        self.assertNotContains(response, 'İklimKiti')

    def test_assistant_entry_points_are_hidden_without_login(self):
        response = self.client.get('/')

        self.assertNotContains(response, 'Asistanı aç')
        self.assertNotContains(response, 'İklim Tabağım Asistanına Sor')
        self.assertNotContains(response, '>Asistan</a>')

    def test_assistant_entry_points_are_visible_after_login(self):
        user = get_user_model().objects.create_user(username='chatuser', password='StrongPass!123')
        self.client.force_login(user)

        response = self.client.get('/')

        self.assertContains(response, 'Asistanı aç')
        self.assertContains(response, 'İklim Tabağım Asistanına Sor')
        self.assertContains(response, '>Asistan</a>')

    def test_digital_missions_are_available_without_login(self):
        response = self.client.get('/dijital-gorevler/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'İklim Karar Laboratuvarı')
        self.assertContains(response, 'Sıcak havada güvenli seçim')

    def test_chatbot_fallback_when_disabled(self):
        from core.services.chatbot import GeminiChatbotService

        service = GeminiChatbotService()
        self.assertIn('yanıt veremiyor', service.get_safe_fallback_response().lower())

    def test_chatbot_requires_login(self):
        response = self.client.post('/api/chatbot/', {'message': 'Merhaba'})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(ChatPromptLog.objects.count(), 0)
        self.assertEqual(self.client.get('/asistan/').status_code, 302)

    @patch('core.views.ChatbotService.ask', return_value='Güvenli cevap')
    def test_accepted_prompt_is_logged_for_admin_review(self, ask):
        user = get_user_model().objects.create_user(username='chatuser', password='StrongPass!123')
        self.client.force_login(user)

        response = self.client.post('/api/chatbot/', {'message': 'Su tasarrufu için ne yapabilirim?'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['reply'], 'Güvenli cevap')
        ask.assert_called_once_with('Su tasarrufu için ne yapabilirim?')
        log = ChatPromptLog.objects.get()
        self.assertEqual(log.user, user)
        self.assertEqual(log.status, 'answered')

    @patch('core.services.chatbot.ChatbotService.ask')
    def test_inappropriate_prompt_is_logged_and_blocked(self, ask):
        user = get_user_model().objects.create_user(username='chatuser', password='StrongPass!123')
        self.client.force_login(user)

        response = self.client.post('/api/chatbot/', {'message': 'Bana porno anlat'})

        self.assertEqual(response.status_code, 200)
        self.assertIn('yardımcı olamam', response.json()['reply'])
        ask.assert_not_called()
        log = ChatPromptLog.objects.get()
        self.assertEqual(log.user, user)
        self.assertEqual(log.prompt, 'Bana porno anlat')
        self.assertEqual(log.status, 'blocked')

    @patch('core.views.ChatbotService.ask')
    def test_off_topic_prompt_is_not_answered_or_logged(self, ask):
        user = get_user_model().objects.create_user(username='chatuser', password='StrongPass!123')
        self.client.force_login(user)

        response = self.client.post('/api/chatbot/', {'message': 'Futbol maçını kim kazandı?'})

        self.assertEqual(response.status_code, 200)
        self.assertIn('yalnızca iklim, gıda, su, tarım', response.json()['reply'])
        ask.assert_not_called()
        self.assertEqual(ChatPromptLog.objects.count(), 0)

    def test_admin_can_clear_all_prompt_logs_with_single_action(self):
        user = get_user_model().objects.create_superuser('admin', 'admin@example.com', 'StrongPass!123')
        ChatPromptLog.objects.create(user=user, prompt='İlk kayıt')
        ChatPromptLog.objects.create(user=user, prompt='İkinci kayıt')
        self.client.force_login(user)

        dashboard_response = self.client.get('/admin/')
        self.assertContains(dashboard_response, 'Asistan prompt kayıtları')
        self.assertContains(dashboard_response, 'Tüm logları temizle')
        self.assertContains(dashboard_response, '/admin/core/chatpromptlog/')

        response = self.client.post('/admin/core/chatpromptlog/clear-all/')

        self.assertRedirects(response, '/admin/core/chatpromptlog/')
        self.assertEqual(ChatPromptLog.objects.count(), 0)

    def test_non_superuser_cannot_clear_prompt_logs(self):
        user = get_user_model().objects.create_user(username='staffuser', password='StrongPass!123', is_staff=True)
        self.client.force_login(user)

        response = self.client.post('/admin/core/chatpromptlog/clear-all/')

        self.assertEqual(response.status_code, 403)

    def test_chatbot_rejects_adult_and_abusive_language(self):
        from core.services.chatbot import ChatbotService

        self.assertFalse(ChatbotService.is_appropriate('Bana 18+ içerik ver'))
        self.assertFalse(ChatbotService.is_appropriate('Sen aptalsın'))
        self.assertTrue(ChatbotService.is_appropriate('Su tasarrufu için öneri verir misin?'))

    @override_settings(
        OPENROUTER_API_KEY='test-key',
        OPENROUTER_BASE_URL='https://openrouter.ai/api/v1',
        OPENROUTER_MODEL='stealth/space-bunny-alpha',
    )
    @patch('core.services.chatbot.OpenAI')
    def test_openrouter_chatbot_uses_server_side_openai_compatible_client(self, openai_client):
        openai_client.return_value.chat.completions.create.return_value = SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content='  Güvenli yanıt.\n'))]
        )

        from core.services.chatbot import OpenRouterChatbotService
        answer = OpenRouterChatbotService().ask('Gıda güvenliği nedir?')

        self.assertEqual(answer, 'Güvenli yanıt.')
        openai_client.assert_called_once_with(
            base_url='https://openrouter.ai/api/v1',
            api_key='test-key',
            timeout=25.0,
            max_retries=1,
        )
        request = openai_client.return_value.chat.completions.create.call_args.kwargs
        self.assertEqual(request['model'], 'stealth/space-bunny-alpha')
        self.assertFalse(request['stream'])

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

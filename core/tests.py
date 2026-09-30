from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from types import SimpleNamespace
from unittest.mock import patch

from core.models import GuideSection, IdeathonGuide


class CoreViewTests(TestCase):
    def test_homepage_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_digital_missions_are_available_without_login(self):
        response = self.client.get('/dijital-gorevler/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'İklim Karar Laboratuvarı')
        self.assertContains(response, 'Sıcak havada güvenli seçim')

    def test_chatbot_fallback_when_disabled(self):
        from core.services.chatbot import GeminiChatbotService

        service = GeminiChatbotService()
        self.assertIn('yanıt veremiyor', service.get_safe_fallback_response().lower())

    @override_settings(
        NVIDIA_API_KEY='test-key',
        NVIDIA_BASE_URL='https://integrate.api.nvidia.com/v1',
        NVIDIA_MODEL='nvidia/llama-3.1-nemotron-safety-guard-8b-v3',
    )
    @patch('core.services.chatbot.OpenAI')
    def test_nvidia_chatbot_uses_server_side_openai_compatible_client(self, openai_client):
        openai_client.return_value.chat.completions.create.return_value = SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content='  Güvenli yanıt.\n'))]
        )

        from core.services.chatbot import NvidiaSafetyGuardChatbotService
        answer = NvidiaSafetyGuardChatbotService().ask('Gıda güvenliği nedir?')

        self.assertEqual(answer, 'Güvenli yanıt.')
        openai_client.assert_called_once_with(
            base_url='https://integrate.api.nvidia.com/v1',
            api_key='test-key',
            timeout=25.0,
            max_retries=1,
        )
        request = openai_client.return_value.chat.completions.create.call_args.kwargs
        self.assertEqual(request['model'], 'nvidia/llama-3.1-nemotron-safety-guard-8b-v3')
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

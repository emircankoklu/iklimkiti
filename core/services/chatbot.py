from __future__ import annotations

import re
from typing import Any

from django.conf import settings

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover
    genai = None

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None


class GeminiChatbotService:
    def __init__(self):
        self.enabled = getattr(settings, 'GEMINI_ENABLED', False)
        self.api_key = getattr(settings, 'GEMINI_API_KEY', '')
        self.model_name = getattr(settings, 'GEMINI_MODEL', 'gemini-1.5-flash')

    def build_system_instruction(self):
        return (
            'Türkçe yanıt ver. Lise öğrencisine uygun, kısa ve anlaşılır dili kullan. '
            'Önce güvenilir platform içeriklerine yönlendir. Bilmediğin bilgiyi uydurma. '
            'Kişiye özel tıbbi, hukuki veya finansal tavsiye verme. Gıda güvenliği risklerinde '
            'resmî kurumlara ve uzmanlara başvurulmasını öner. Kişisel veri isteme. '
            'Kullanıcının e-posta, şifre, kimlik veya özel bilgilerini isteme. '
            'Zararlı veya tehlikeli talimat vermeme. Sonunda gerektiğinde "Bu yanıt eğitim amaçlıdır." ifadesi kullan.'
        )

    def validate_question(self, question: str) -> str:
        if not question or not question.strip():
            raise ValueError('Boş mesaj gönderilemez.')
        question = question.strip()
        if len(question) > getattr(settings, 'GEMINI_MAX_INPUT_LENGTH', 1000):
            raise ValueError('Mesaj çok uzun.')
        return question

    def get_safe_fallback_response(self):
        return 'İklimKiti Asistanı şu anda yanıt veremiyor. Lütfen daha sonra tekrar deneyin veya konu sayfalarındaki güvenilir kaynakları inceleyin.'

    def ask(self, question: str, context: str | None = None) -> str:
        try:
            question = self.validate_question(question)
        except ValueError:
            raise

        if not self.enabled or not self.api_key or genai is None:
            return self.get_safe_fallback_response()

        try:
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model_name)
            prompt = self.build_system_instruction()
            if context:
                prompt += f' Bağlam: {context}'
            prompt += f' Kullanıcı sorusu: {question}'
            response = model.generate_content(prompt, generation_config={'max_output_tokens': getattr(settings, 'GEMINI_MAX_OUTPUT_TOKENS', 500)})
            text = getattr(response, 'text', '')
            if not text:
                return self.get_safe_fallback_response()
            return re.sub(r'\s+', ' ', text).strip()
        except Exception:
            return self.get_safe_fallback_response()


class NvidiaSafetyGuardChatbotService:
    def __init__(self):
        self.api_key = getattr(settings, 'NVIDIA_API_KEY', '')
        self.base_url = getattr(settings, 'NVIDIA_BASE_URL', 'https://integrate.api.nvidia.com/v1')
        self.model_name = getattr(settings, 'NVIDIA_MODEL', 'nvidia/llama-3.1-nemotron-safety-guard-8b-v3')

    def ask(self, question: str) -> str:
        try:
            question = GeminiChatbotService().validate_question(question)
        except ValueError:
            raise

        if not self.api_key or OpenAI is None:
            return GeminiChatbotService().get_safe_fallback_response()

        try:
            client = OpenAI(
                base_url=self.base_url,
                api_key=self.api_key,
                timeout=25.0,
                max_retries=1,
            )
            completion = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        'role': 'system',
                        'content': (
                            'Türkçe yanıt ver. Lise öğrencisine uygun, kısa ve anlaşılır bir dil kullan. '
                            'Gıda güvenliği, iklim, su ve sürdürülebilir yaşam sorularında güvenilir ve '
                            'temkinli ol; bilmediğin bilgiyi uydurma. Kişisel tıbbi tavsiye verme; riskli '
                            'gıda durumlarında resmî kaynaklara ve güvenilir bir yetişkine yönlendir. '
                            'Zararlı, yasa dışı veya tehlikeli isteklere yardımcı olma; kısa ve sakin '
                            'biçimde reddedip güvenli bir alternatif öner. Kullanıcıdan kişisel bilgi isteme.'
                        ),
                    },
                    {'role': 'user', 'content': question},
                ],
                max_tokens=getattr(settings, 'NVIDIA_MAX_OUTPUT_TOKENS', 500),
                stream=False,
            )
            answer = completion.choices[0].message.content
            if not answer or not answer.strip():
                return GeminiChatbotService().get_safe_fallback_response()
            return re.sub(r'\s+', ' ', answer).strip()
        except Exception:
            return GeminiChatbotService().get_safe_fallback_response()


class ChatbotService:
    """Use NVIDIA when configured; keep the existing Gemini provider as fallback."""

    def ask(self, question: str) -> str:
        if getattr(settings, 'NVIDIA_API_KEY', ''):
            return NvidiaSafetyGuardChatbotService().ask(question)
        return GeminiChatbotService().ask(question)

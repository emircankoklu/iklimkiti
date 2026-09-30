from __future__ import annotations

import re
from typing import Any

from django.conf import settings

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover
    genai = None


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

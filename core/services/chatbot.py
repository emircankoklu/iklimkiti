from __future__ import annotations

import re
import unicodedata
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
            '+18, cinsel içerik, hakaret veya küfür üretme; bu tür talepleri kısa ve nazikçe reddet. '
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


class OpenRouterChatbotService:
    def __init__(self):
        self.api_key = getattr(settings, 'OPENROUTER_API_KEY', '')
        self.base_url = getattr(settings, 'OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')
        self.model_name = getattr(settings, 'OPENROUTER_MODEL', 'stealth/space-bunny-alpha')

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
                            'Yalnızca kullanıcıya yönelik nihai yanıtı ver; düşünme sürecini veya iç muhakemeni yazma. '
                            '+18, cinsel içerik, hakaret veya küfür üretme; bu tür talepleri kısa ve nazikçe reddet. '
                            'Gıda güvenliği, iklim, su ve sürdürülebilir yaşam sorularında güvenilir ve '
                            'temkinli ol; bilmediğin bilgiyi uydurma. Kişisel tıbbi tavsiye verme; riskli '
                            'gıda durumlarında resmî kaynaklara ve güvenilir bir yetişkine yönlendir. '
                            'Zararlı, yasa dışı veya tehlikeli isteklere yardımcı olma; kısa ve sakin '
                            'biçimde reddedip güvenli bir alternatif öner. Kullanıcıdan kişisel bilgi isteme.'
                        ),
                    },
                    {'role': 'user', 'content': question},
                ],
                max_tokens=getattr(settings, 'OPENROUTER_MAX_OUTPUT_TOKENS', 500),
                stream=False,
            )
            answer = completion.choices[0].message.content
            if not answer or not answer.strip():
                return GeminiChatbotService().get_safe_fallback_response()
            answer = self.remove_reasoning_text(answer)
            if not answer:
                return GeminiChatbotService().get_safe_fallback_response()
            return re.sub(r'\s+', ' ', answer).strip()
        except Exception:
            return GeminiChatbotService().get_safe_fallback_response()

    @staticmethod
    def remove_reasoning_text(answer: str) -> str:
        """Hide model reasoning when a reasoning-capable model includes it in content."""
        answer = re.sub(r'<think>.*?</think>', '', answer, flags=re.IGNORECASE | re.DOTALL)
        answer = re.sub(r'<thinking>.*?</thinking>', '', answer, flags=re.IGNORECASE | re.DOTALL)

        markers = (
            r"Here's the final answer:",
            r'Here is the final answer:',
            r'Final answer:',
            r'Yanıt:',
            r'Cevap:',
        )
        lower_answer = answer.lower()
        marker_positions = [
            (lower_answer.find(marker.lower()), len(marker))
            for marker in markers
            if lower_answer.find(marker.lower()) >= 0
        ]
        if marker_positions:
            position, marker_length = min(marker_positions)
            answer = answer[position + marker_length:]
        else:
            thinking_markers = (
                "Here's a thinking process:",
                'Here is a thinking process:',
                'Thinking process:',
                'Düşünme süreci:',
            )
            lower_answer = answer.lower()
            positions = [
                lower_answer.find(marker.lower())
                for marker in thinking_markers
                if lower_answer.find(marker.lower()) >= 0
            ]
            if positions:
                answer = answer[:min(positions)]

        return answer.strip()


class ChatbotService:
    """Use OpenRouter when configured; keep the existing Gemini provider as fallback."""

    REFUSAL_RESPONSE = 'Bu tür ifadeler veya +18 içerikler konusunda yardımcı olamam. Lütfen saygılı ve güvenli bir dille, iklim ya da gıda konularında soru sor.'
    BLOCKED_TERMS = {
        'adult', 'anal', 'asshole', 'bastard', 'bitch', 'blowjob', 'boob', 'breast',
        'cock', 'dick', 'fuck', 'hentai', 'nsfw', 'porno', 'porn', 'sex', 'sexual',
        'sexting', 'shit', 'slut', 'tits', 'siktir', 'sikik', 'sikim', 'siker',
        'sikeyim', 'sikiyor', 'sikmek', 'sik', 'orospu', 'pic', 'piç', 'yarrak',
        'amcik', 'amcık', 'amk', 'aq', 'oç', 'oc', 'salak', 'aptal', 'gerizekali',
        'gerizekalı', 'mal', 'embesil', 'pezevenk', 'ibne', 'kahpe',
        'çıplak', 'ciplak', 'nude', 'onlyfans', 'masturbasyon', 'mastürbasyon',
        'vajina', 'penis', 'orgazm', 'erotik',
    }

    @classmethod
    def is_appropriate(cls, text: str) -> bool:
        if re.search(r'\b18\s*(?:\+|plus)', text.casefold()):
            return False
        normalized = unicodedata.normalize('NFKD', text).casefold()
        normalized = ''.join(char for char in normalized if not unicodedata.combining(char))
        normalized = normalized.translate(str.maketrans({'0': 'o', '3': 'e', '4': 'a', '@': 'a', '$': 's'}))
        words = re.findall(r'[a-z0-9]+', normalized)
        if 'yetiskin icerik' in normalized:
            return False
        return not any(
            word in cls.BLOCKED_TERMS or any(
                len(term) >= 5 and word.startswith(term)
                for term in cls.BLOCKED_TERMS
            )
            for word in words
        )

    def ask(self, question: str) -> str:
        question = GeminiChatbotService().validate_question(question)
        if not self.is_appropriate(question):
            return self.REFUSAL_RESPONSE

        if getattr(settings, 'OPENROUTER_API_KEY', ''):
            response = OpenRouterChatbotService().ask(question)
        else:
            response = GeminiChatbotService().ask(question)
        if not self.is_appropriate(response):
            return self.REFUSAL_RESPONSE
        return response

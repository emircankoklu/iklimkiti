from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

from django.conf import settings

from core.services.chatbot import (
    GeminiChatbotService,
    NvidiaSafetyGuardChatbotService,
    OpenRouterChatbotService,
)

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover
    genai = None

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None


@dataclass
class InvoiceImageResult:
    status: str
    message: str
    values: dict[str, float]


class InvoiceAnalysisService:
    """Validate invoice images and extract utility readings with Gemini when enabled."""

    ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png', 'image/webp'}
    MAX_FILE_SIZE = 8 * 1024 * 1024
    FALLBACK_MESSAGE = 'Görsel yüklendi; AI doğrulaması yapılamadığı için fatura türü manuel kontrol bekliyor.'

    def generate_personalized_analysis(self, profile: dict, carbon: float, period_days: int) -> tuple[str, bool]:
        prompt = (
            'Ev enerji ve su tüketimi için Türkçe, kişiye özel ve uygulanabilir bir değerlendirme yaz. '
            'En fazla 3 kısa paragraf ve sonunda "İlk adım:" ile başlayan tek bir öneri ver. '
            'Kullanıcının kat konumu, hane büyüklüğü, duş sıklığı, tüketim dağılımı ve karbon tahminini '
            'birlikte yorumla. Sayıları değiştirme, tıbbi/finansal tavsiye verme, suçlayıcı olma. '
            f'Profil: kat={profile["floor_position"]}, kişi={profile["household_size"]}, '
            f'duş/hafta={profile["showers_per_week"]}; elektrik={profile["electricity"]} kWh, '
            f'gaz={profile["gas"]} m³, su={profile["water"]} m³, dönem={period_days} gün, '
            f'tahmini karbon={carbon:.1f} kg CO2e.'
        )
        provider = getattr(settings, 'INVOICE_AI_PROVIDER', 'gemini')
        try:
            if provider == 'nvidia' and getattr(settings, 'NVIDIA_API_KEY', ''):
                result = NvidiaSafetyGuardChatbotService().ask(prompt)
            elif provider == 'openrouter' and getattr(settings, 'OPENROUTER_API_KEY', ''):
                result = OpenRouterChatbotService().ask(prompt)
            elif getattr(settings, 'GEMINI_API_KEY', ''):
                result = GeminiChatbotService().ask(prompt)
            else:
                return self._fallback_personalized_analysis(profile, carbon), False
            if result and 'yanıt veremiyor' not in result.lower():
                return result, True
        except (ValueError, TypeError, OSError):
            pass
        return self._fallback_personalized_analysis(profile, carbon), False

    @staticmethod
    def _fallback_personalized_analysis(profile: dict, carbon: float) -> str:
        floor_text = {'bottom': 'en alt katta', 'middle': 'ara katta', 'top': 'en üst katta'}[profile['floor_position']]
        largest = max(
            (('elektrik', profile['electricity']), ('gaz', profile['gas']), ('su', profile['water'])),
            key=lambda item: item[1],
        )[0]
        return (
            f'{profile["household_size"]} kişilik hanen için {floor_text} yaşamanın ısıtma davranışına '
            f'etkisini ve haftada {profile["showers_per_week"]} duş alışkanlığını birlikte değerlendirdik. '
            f'Yaklaşık {carbon:.1f} kg CO2e tahmininde en yüksek pay {largest} tüketiminde görünüyor. '
            f'İlk adım: Bu hafta {largest} tüketimini her gün aynı saatte kontrol et ve bir sonraki dönemde '
            f'küçük ama ölçülebilir bir düşüş hedefle.'
        )

    def analyze_image(self, image_file) -> InvoiceImageResult:
        self.validate_image(image_file)
        provider = getattr(settings, 'INVOICE_AI_PROVIDER', 'gemini')
        if provider == 'nvidia':
            return self._analyze_with_nvidia(image_file)
        if not getattr(settings, 'GEMINI_API_KEY', '') or genai is None:
            return InvoiceImageResult('review', self.FALLBACK_MESSAGE, {})

        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel(getattr(settings, 'GEMINI_MODEL', 'gemini-1.5-flash'))
            prompt = self._analysis_prompt()
            response = model.generate_content([
                prompt,
                {'mime_type': image_file.content_type, 'data': image_file.read()},
            ])
            data = self._parse_response(getattr(response, 'text', ''))
        except (ValueError, TypeError, OSError, json.JSONDecodeError):
            return InvoiceImageResult('review', self.FALLBACK_MESSAGE, {})

        if not data.get('is_invoice'):
            return InvoiceImageResult('invalid', 'Bu görsel fatura olarak doğrulanamadı. Lütfen net bir elektrik, gaz veya su faturası yükleyin.', {})
        values = {
            key: float(data[key])
            for key in ('consumption', 'amount', 'period_days')
            if isinstance(data.get(key), (int, float)) and data[key] >= 0
        }
        return InvoiceImageResult('verified', 'Fatura görseli AI tarafından doğrulandı.', values)

    def _analyze_with_nvidia(self, image_file) -> InvoiceImageResult:
        api_key = getattr(settings, 'NVIDIA_API_KEY', '')
        if not api_key or OpenAI is None:
            return InvoiceImageResult('review', self.FALLBACK_MESSAGE, {})
        try:
            import base64

            encoded = base64.b64encode(image_file.read()).decode('ascii')
            client = OpenAI(
                base_url=getattr(settings, 'NVIDIA_BASE_URL', 'https://integrate.api.nvidia.com/v1'),
                api_key=api_key,
                timeout=30.0,
                max_retries=1,
            )
            completion = client.chat.completions.create(
                model=getattr(settings, 'NVIDIA_INVOICE_MODEL', 'meta/llama-3.2-90b-vision-instruct'),
                messages=[{
                    'role': 'user',
                    'content': [
                        {'type': 'text', 'text': self._analysis_prompt()},
                        {'type': 'image_url', 'image_url': {'url': f'data:{image_file.content_type};base64,{encoded}'}},
                    ],
                }],
                max_tokens=getattr(settings, 'NVIDIA_INVOICE_MAX_OUTPUT_TOKENS', 300),
                stream=False,
            )
            data = self._parse_response(completion.choices[0].message.content or '')
        except (ValueError, TypeError, OSError, json.JSONDecodeError):
            return InvoiceImageResult('review', self.FALLBACK_MESSAGE, {})
        if not data.get('is_invoice'):
            return InvoiceImageResult('invalid', 'Bu görsel fatura olarak doğrulanamadı. Lütfen net bir elektrik, gaz veya su faturası yükleyin.', {})
        values = {
            key: float(data[key])
            for key in ('consumption', 'amount', 'period_days')
            if isinstance(data.get(key), (int, float)) and data[key] >= 0
        }
        return InvoiceImageResult('verified', 'Fatura görseli NVIDIA AI tarafından doğrulandı.', values)

    @staticmethod
    def _analysis_prompt() -> str:
        return (
            'Bu görsel bir elektrik, doğal gaz veya su faturası mı? '
            'Sadece JSON döndür: {"is_invoice":true/false,"type":"electricity|gas|water|unknown",'
            '"consumption":number|null,"amount":number|null,"period_days":number|null}. '
            'Fatura değilse tüm sayısal alanları null yap. Tüketim birimini değiştirme.'
        )

    @classmethod
    def validate_image(cls, image_file) -> None:
        if not image_file:
            raise ValueError('Fatura görseli eksik.')
        if image_file.size > cls.MAX_FILE_SIZE:
            raise ValueError('Her fatura görseli en fazla 8 MB olabilir.')
        if image_file.content_type not in cls.ALLOWED_MIME_TYPES:
            raise ValueError('Yalnızca JPG, PNG veya WEBP fatura görselleri yükleyebilirsiniz.')

        from PIL import Image

        image_file.seek(0)
        try:
            with Image.open(image_file) as image:
                image.verify()
        except (OSError, ValueError) as exc:
            raise ValueError('Yüklenen dosya geçerli bir görsel değil.') from exc
        image_file.seek(0)

    @staticmethod
    def _parse_response(text: str) -> dict[str, Any]:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if not match:
            raise ValueError('AI yanıtı JSON içermiyor.')
        return json.loads(match.group(0))

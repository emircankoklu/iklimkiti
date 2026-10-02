from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST

from core.services.chatbot import ChatbotService
from core.services.invoice_analysis import InvoiceAnalysisService
from core.models import ChatPromptLog, HomePageContent, IdeathonGuide
from games.models import MiniGame
from learning.models import GlossaryTerm, MindMap, QuestionAnswer, Topic


def home(request):
    homepage, _ = HomePageContent.objects.get_or_create(pk=1)
    topics = Topic.objects.filter(is_published=True)[:6]
    games = MiniGame.objects.filter(is_published=True, status='ready').exclude(game_type='matching')[:4]
    maps = MindMap.objects.filter(is_published=True)[:3]
    terms = GlossaryTerm.objects.filter(is_published=True)[:6]
    question_answers = QuestionAnswer.objects.filter(is_published=True).select_related('topic')[:4]
    return render(request, 'home.html', {'topics': topics, 'games': games, 'maps': maps, 'terms': terms, 'question_answers': question_answers, 'homepage': homepage})


def digital_missions(request):
    return render(request, 'digital_missions.html')


def about(request):
    return render(request, 'about.html')


def references(request):
    from learning.models import Source

    sources = Source.objects.filter(is_verified=True)[:12]
    return render(request, 'references.html', {'sources': sources})


@staff_member_required
def admin_cop31_guide(request):
    guide = IdeathonGuide.objects.filter(is_published=True).prefetch_related('sections').first()
    return render(request, 'admin/cop31_guide.html', {'guide': guide})


@staff_member_required
def admin_ai_providers(request):
    def configured(key):
        value = getattr(settings, key, '')
        return bool(value)

    return render(request, 'admin/ai_providers.html', {
        'provider': getattr(settings, 'INVOICE_AI_PROVIDER', 'gemini'),
        'providers': [
            {
                'name': 'Google Gemini',
                'key_name': 'GEMINI_API_KEY',
                'configured': configured('GEMINI_API_KEY'),
                'model': getattr(settings, 'GEMINI_MODEL', ''),
                'endpoint': 'Google Generative AI SDK',
                'active': getattr(settings, 'INVOICE_AI_PROVIDER', 'gemini') == 'gemini',
                'note': 'Gemini 1.5/2.0 Flash ve görsel anlayan modeller fatura analizi için uygundur.',
            },
            {
                'name': 'NVIDIA NIM',
                'key_name': 'NVIDIA_API_KEY',
                'configured': configured('NVIDIA_API_KEY'),
                'model': getattr(settings, 'NVIDIA_INVOICE_MODEL', ''),
                'endpoint': getattr(settings, 'NVIDIA_BASE_URL', ''),
                'active': getattr(settings, 'INVOICE_AI_PROVIDER', 'gemini') == 'nvidia',
                'note': 'OpenAI uyumlu NVIDIA NIM endpointi ve görsel destekli bir model gerekir.',
            },
        ],
    })


@login_required
def assistant_view(request):
    return render(request, 'assistant.html')


@login_required
def invoice_analysis_view(request):
    return render(request, 'invoice_analysis.html')


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)


@require_POST
def chatbot_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Asistanı kullanmak için giriş yapmalısınız.', 'login_url': reverse('login')}, status=401)

    message = (request.POST.get('message') or '').strip()
    if not message:
        return JsonResponse({'error': 'Boş mesaj gönderilemez.'}, status=400)
    if len(message) > 1000:
        return JsonResponse({'error': 'Mesaj çok uzun.'}, status=400)

    service = ChatbotService()
    if not service.is_appropriate(message):
        ChatPromptLog.objects.create(
            user=request.user,
            prompt=message,
            status='blocked',
        )
        return JsonResponse({'reply': service.REFUSAL_RESPONSE})
    if not service.is_on_topic(message):
        return JsonResponse({'reply': service.SCOPE_RESPONSE})

    prompt_log = ChatPromptLog.objects.create(
        user=request.user,
        prompt=message,
        status='received',
    )
    service = ChatbotService()
    if not service.is_appropriate(message):
        prompt_log.status = 'blocked'
        prompt_log.save(update_fields=['status'])
        return JsonResponse({'reply': service.REFUSAL_RESPONSE})

    try:
        response = service.ask(message)
    except ValueError as exc:
        return JsonResponse({'error': str(exc)}, status=400)
    prompt_log.status = 'answered'
    prompt_log.save(update_fields=['status'])
    return JsonResponse({'reply': response})


@login_required
@require_POST
def invoice_analysis_api(request):
    try:
        floor_position = request.POST.get('floor_position', '')
        household_size = int(request.POST.get('household_size', '0'))
        showers_per_week = int(request.POST.get('showers_per_week', '0'))
        if floor_position not in {'bottom', 'middle', 'top'}:
            raise ValueError('Kat konumu seçimi geçersiz.')
        if not 1 <= household_size <= 6:
            raise ValueError('Evde yaşayan kişi sayısı 1-6 arasında olmalıdır.')
        if not 1 <= showers_per_week <= 14:
            raise ValueError('Duş sıklığı haftada 1-14 arasında olmalıdır.')

        e_invoice = request.POST.get('e_invoice') == 'on'
        if e_invoice:
            for field in ('electricity_consumption', 'gas_consumption', 'water_consumption'):
                value = float(request.POST.get(field, ''))
                if value < 0:
                    raise ValueError('Fatura tüketim değerleri negatif olamaz.')
        files = [request.FILES.get(name) for name in ('electricity_bill', 'gas_bill', 'water_bill')]
        if any(file is None for file in files):
            raise ValueError('Elektrik, gaz ve su için üç fatura görseli de yüklenmelidir.')

        service = InvoiceAnalysisService()
        analyses = [service.analyze_image(file) for file in files]
        invalid = [analysis.message for analysis in analyses if analysis.status == 'invalid']
        if invalid:
            return JsonResponse({'error': ' '.join(invalid)}, status=422)

        consumption = {}
        field_names = ('electricity', 'gas', 'water')
        for name, analysis in zip(field_names, analyses):
            form_value = request.POST.get(f'{name}_consumption', '')
            if e_invoice and form_value:
                consumption[name] = float(form_value)
            else:
                consumption[name] = analysis.values.get('consumption', 0)
        if not any(consumption.values()):
            # Keep the no-API-key demo useful while clearly marking image results for review.
            consumption = {
                'electricity': 150 * household_size,
                'gas': 35 * household_size,
                'water': 3 * household_size,
            }

        period_days = max(
            [analysis.values.get('period_days', 30) for analysis in analyses if analysis.values.get('period_days')] or [30]
        )
        carbon = (
            consumption['electricity'] * 0.42
            + consumption['gas'] * 2.0
            + consumption['water'] * 0.344
        )
        per_person = carbon / household_size
        shower_factor = max(0.75, 1 - max(0, showers_per_week - 3) * 0.02)
        daily = carbon / period_days
        weekly = daily * 7
        monthly_target = carbon * 0.9 * shower_factor
        verified_count = sum(analysis.status == 'verified' for analysis in analyses)
        recommendations = [
            f'Elektrik: haftada iki kez çamaşır ve bulaşık makinesini tam dolu çalıştır; aylık yaklaşık %{min(18, 8 + household_size * 2)} tasarruf hedefle.',
            f'Gaz: termostatı 1°C düşür ve ara kattaysan ısıyı komşu dairelerden destekle; günlük {max(0.1, consumption["gas"] / period_days * 0.08):.1f} m³ azaltmayı dene.',
            f'Su: duşu kişi başına 5 dakika ile sınırla; haftalık {max(20, household_size * 35)} litre su tasarrufu hedefle.',
        ]
        return JsonResponse({
            'carbon': round(carbon, 1),
            'per_person_carbon': round(per_person, 1),
            'verified_count': verified_count,
            'review_count': 3 - verified_count,
            'invoice_messages': [analysis.message for analysis in analyses],
            'targets': {
                'daily': round(daily * 0.95, 1),
                'weekly': round(weekly * 0.92, 1),
                'monthly': round(monthly_target, 1),
            },
            'recommendations': recommendations,
            'comparison': f'Bu tahmin, evinizin mevcut dönemdeki yaklaşık {carbon:.1f} kg CO₂e tüketimini temel alır. Kişi başına {per_person:.1f} kg CO₂e düşüyor.',
        })
    except (TypeError, ValueError) as exc:
        return JsonResponse({'error': str(exc)}, status=400)


def assistant_chat(request):
    return assistant_view(request)

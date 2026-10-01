from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST

from core.services.chatbot import ChatbotService
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


@login_required
def assistant_view(request):
    return render(request, 'assistant.html')


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


def assistant_chat(request):
    return assistant_view(request)

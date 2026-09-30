import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from games.engine import GameRegistry
from games.models import GameProgress, MiniGame
from games.services import complete_game_for_user, get_user_progress


def game_list(request):
    queryset = MiniGame.objects.filter(is_published=True)
    query = request.GET.get('q', '').strip()
    if query:
        queryset = queryset.filter(title__icontains=query)
    return render(request, 'games/game_list.html', {'games': queryset, 'query': query})


def game_detail(request, slug):
    game = get_object_or_404(MiniGame, slug=slug, is_published=True)
    if game.status == 'placeholder':
        return render(request, 'games/game_placeholder.html', {'game': game})
    if not request.user.is_authenticated:
        return render(request, 'games/game_login_required.html', {'game': game})

    registry = GameRegistry()
    engine = registry.get(game.game_type)
    return render(request, 'games/game_play.html', {'game': game, 'engine': engine, 'progress': get_user_progress(request.user).filter(game=game).first()})


@require_http_methods(['POST'])
def game_submit(request, slug):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Giriş gerekli'}, status=401)

    game = get_object_or_404(MiniGame, slug=slug, is_published=True)
    if game.status != 'ready':
        return JsonResponse({'error': 'Bu oyun şu anda aktif değil.'}, status=400)

    submitted = request.POST.get('answers', '{}')
    try:
        answers = json.loads(submitted)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Geçersiz cevap formatı.'}, status=400)

    engine = GameRegistry().get(game.game_type)
    result = engine.evaluate(game, answers)
    progress = complete_game_for_user(request.user, game, result)
    if result.passed:
        messages.success(request, 'Oyun tamamlandı! İlerleme ve rozetler güncellendi.')
    else:
        messages.info(request, 'Oyun tamamlanamadı; tekrar deneyebilirsiniz.')

    return JsonResponse({
        'passed': result.passed,
        'score': result.score,
        'message': result.message,
        'progress': {
            'status': progress.status if progress else 'started',
            'score': progress.score if progress else 0,
        },
    })


def game_progress(request):
    if not request.user.is_authenticated:
        return render(request, 'games/game_login_required.html', {'game': None})
    user_progress = GameProgress.objects.filter(user=request.user).select_related('game')
    return render(request, 'games/game_progress.html', {'progress': user_progress})

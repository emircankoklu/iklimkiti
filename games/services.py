from __future__ import annotations

from django.db import transaction
from django.utils import timezone

from badges.models import Badge, UserBadge
from games.models import GameProgress


def complete_game_for_user(user, game, result):
    if not game.can_be_completed():
        return None
    with transaction.atomic():
        progress, _ = GameProgress.objects.get_or_create(user=user, game=game)
        if progress.status != 'completed':
            progress.status = 'completed'
        progress.score = max(progress.score, int(result.score))
        progress.attempts_count += 1
        progress.completed_at = timezone.now()
        progress.last_played_at = timezone.now()
        progress.save(update_fields=['status', 'score', 'attempts_count', 'completed_at', 'last_played_at', 'updated_at'])
        award_badges_for_game_completion(user, game, result)
        return progress


def award_badges_for_game_completion(user, game, result):
    if not result.passed:
        return []
    earned = []
    badges = Badge.objects.filter(is_active=True)
    for badge in badges:
        if badge.required_game and badge.required_game_id == game.id:
            obj, created = UserBadge.objects.get_or_create(user=user, badge=badge)
            if created:
                earned.append(obj)
        if badge.required_topic and badge.required_topic_id == game.topic_id and badge.badge_type == 'topic_completed':
            obj, created = UserBadge.objects.get_or_create(user=user, badge=badge)
            if created:
                earned.append(obj)
    if not any(listed for listed in earned):
        first_badge = Badge.objects.filter(is_active=True, badge_type='first_game').first()
        if first_badge and not UserBadge.objects.filter(user=user, badge=first_badge).exists():
            user_badge = UserBadge.objects.create(user=user, badge=first_badge)
            earned.append(user_badge)
    return earned


def get_user_progress(user):
    return GameProgress.objects.filter(user=user).select_related('game')

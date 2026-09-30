import json

from django.contrib.auth import get_user_model
from django.db import models

from learning.models import Topic, slugify_turkish

User = get_user_model()


class MiniGame(models.Model):
    GAME_TYPE_CHOICES = [
        ('multiple_choice', 'Çoktan Seçmeli'),
        ('true_false', 'Doğru/Yanlış'),
        ('matching', 'Eşleştirme'),
        ('scenario', 'Senaryo'),
    ]
    STATUS_CHOICES = [
        ('planned', 'Planlandı'),
        ('placeholder', 'Yakında'),
        ('ready', 'Hazır'),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='games')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    game_type = models.CharField(max_length=30, choices=GAME_TYPE_CHOICES, default='multiple_choice')
    difficulty = models.CharField(max_length=20, default='medium')
    estimated_duration_seconds = models.PositiveIntegerField(default=180)
    thumbnail = models.ImageField(upload_to='games/thumbnails/', blank=True, null=True)
    configuration_json = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_turkish(self.title)
        if self.configuration_json:
            if isinstance(self.configuration_json, str):
                self.configuration_json = json.loads(self.configuration_json)
        super().save(*args, **kwargs)

    def can_be_completed(self):
        return self.status == 'ready'

    def get_questions(self):
        if not isinstance(self.configuration_json, dict):
            return []
        return self.configuration_json.get('questions', [])

    def __str__(self):
        return self.title


class GameProgress(models.Model):
    STATUS_CHOICES = [
        ('started', 'Başladı'),
        ('completed', 'Tamamlandı'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gameprogress_set')
    game = models.ForeignKey(MiniGame, on_delete=models.CASCADE, related_name='progress')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='started')
    score = models.PositiveIntegerField(default=0)
    attempts_count = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_played_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'game'], name='unique_game_progress_per_user_game')]

    def __str__(self):
        return f'{self.user.username} - {self.game.title}'


class GameAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempts')
    game = models.ForeignKey(MiniGame, on_delete=models.CASCADE, related_name='attempts')
    submitted_answers = models.JSONField(default=dict, blank=True)
    score = models.PositiveIntegerField(default=0)
    passed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} : {self.game.title}'

from django.contrib.auth import get_user_model
from django.db import models

from games.models import MiniGame
from learning.models import Topic, slugify_turkish

User = get_user_model()


class Badge(models.Model):
    BADGE_TYPE_CHOICES = [
        ('first_game', 'İlk Oyun'),
        ('game_completed', 'Oyun Tamamlandı'),
        ('topic_completed', 'Konu Tamamlandı'),
        ('food_safety', 'Gıda Güvenliği'),
        ('food_waste', 'Gıda İsrafı'),
        ('water_awareness', 'Su Bilinci'),
        ('sustainable_agriculture', 'Sürdürülebilir Tarım'),
        ('climate_explorer', 'İklim Kaşifi'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, default='🏆')
    color = models.CharField(max_length=20, default='#37D67A')
    badge_type = models.CharField(max_length=40, choices=BADGE_TYPE_CHOICES, default='game_completed')
    required_game = models.ForeignKey(MiniGame, on_delete=models.SET_NULL, null=True, blank=True, related_name='required_badges')
    required_topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='badges')
    required_count = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_turkish(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='awarded_users')
    earned_at = models.DateTimeField(auto_now_add=True)
    metadata_json = models.JSONField(default=dict, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'badge'], name='unique_user_badge')]

    def __str__(self):
        return f'{self.user.username} - {self.badge.name}'

from django.contrib import admin

from badges.models import Badge, UserBadge


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
	list_display = ('name', 'badge_type', 'required_count', 'is_active', 'updated_at')
	list_filter = ('badge_type', 'is_active')
	search_fields = ('name', 'description', 'required_game__title', 'required_topic__title')
	autocomplete_fields = ('required_game', 'required_topic')
	prepopulated_fields = {'slug': ('name',)}


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
	list_display = ('user', 'badge', 'earned_at')
	list_filter = ('badge',)
	search_fields = ('user__username', 'badge__name')
	autocomplete_fields = ('user', 'badge')
	readonly_fields = ('earned_at',)
